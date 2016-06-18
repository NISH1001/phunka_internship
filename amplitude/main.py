#!/usr/bin/env python3

from amplitude import AmplitudeClass
import settings

def main():
    amp = AmplitudeClass(settings.API_KEY, settings.SECRET_KEY, "20160604", "20160604")

    print(amp.get_response())
    if amp.get_response() == 200:
        amp.extract()
        print(amp.get_current_path())
        data = amp.read_json_all(amp.get_current_path())
        amp.createdb()
        amp.insert_all()
        #amp.query_all()
        #amp.query_single( {'uuid':"238f666a-2eca-11e6-b6a6-22000a5981c8"} )

if __name__ == "__main__":
    main()

