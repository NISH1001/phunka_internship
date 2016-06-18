#!/usr/bin/env python3

import datetime
from amplitude import AmplitudeClass
import settings

def main():
    start_date = datetime.date(2016, 1, 1)
    delta_days = 5
    final_date = datetime.date.today()
    while start_date <= final_date:
        start = start_date.strftime("%Y%m%d")
        start_date += datetime.timedelta(days=delta_days)
        end = start_date.strftime("%Y%m%d")
        print("start : {} || end : {}".format(start, end))
        amp = AmplitudeClass(settings.API_KEY, settings.SECRET_KEY, start, end)
        print("status code : ", amp.get_response())
        if amp.get_response() == 200:
            amp.extract()
            print("extracting to : ", amp.get_current_path())
            data = amp.read_json_all(amp.get_current_path())
            amp.createdb()
            amp.insert_all()
            #amp.query_all()
            #amp.query_single( {'uuid':"238f666a-2eca-11e6-b6a6-22000a5981c8"} )
        print('-' * 40)

if __name__ == "__main__":
    main()

