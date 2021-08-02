import traceback
import json
import sys


class DummyBackend:
    def __init__(self, rd, wr):
        self._rd = rd
        self._wr = wr

        # tmp. memory we use to mock up a backend
        self._last_parameter = None

    def process_request(self):
        in_request = False
        request = ""
        for line in self._rd:
            # Remove trailing newline
            line = line.decode('UTF-8').rstrip()
            if line == "#request begin":
                in_request = True
            elif line == "#request end":
                try:
                    self._process(request)
                except Exception:
                    tb = traceback.format_exc()
                    print("You should look into this:\n", tb, file=sys.stderr)
                    self._respond("BackendError", {"msg": tb})
                return True
            else:
                if in_request:
                    request = request + line
        return False

    def _respond(self, name, data=None):
        if data is None:
            data = {}
        response = {"name": name, "data": data}
        response = json.dumps(response)
        self._wr.write(b"#response begin\n")
        self._wr.write(bytes(response+"\n", "utf-8"))
        self._wr.write(b"#response end\n")
        self._wr.flush()

    def _process(self, request):
        request = json.loads(request)
        name = request.get("name")
        data = request.get("data")
        assert isinstance(data, dict)

        if name == "GetFeatures":
            self._respond("FeatureList", {"features": []})

        elif name == "StartTest":
            test_name = data.get("testName")
            if test_name != ("neo4j.datatypes.TestDataTypes."
                             "test_should_echo_back"):
                self._respond("SkipTest", {"reason": "This is just a mock."})
            else:
                self._respond("RunTest")

        elif name == "NewDriver":
            self._respond("Driver", {"id": 1})

        elif name == "NewSession":
            self._respond("Session", {"id": 1})

        elif name == "SessionRun":
            cypher = data.get("cypher")
            assert cypher == "RETURN $x as y"
            params = data.get("params")
            assert isinstance(params, dict)
            assert list(params) == ["x"]
            self._last_parameter = next(iter(params.values()))
            self._respond("Result", {"id": 1, "keys": ["y"]})

        elif name == "ResultNext":
            if self._last_parameter is None:
                self._respond("NullRecord")
            else:
                self._respond("Record", {"values": [self._last_parameter]})
                self._last_parameter = None

        elif name == "SessionClose":
            self._respond("Session", {"id": 1})

        elif name == "DriverClose":
            self._respond("Driver", {"id": 1})




