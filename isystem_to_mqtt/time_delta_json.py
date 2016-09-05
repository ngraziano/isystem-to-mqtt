""" Custom Json encoder """

import datetime
from json import JSONEncoder


class CustomDateJSONEncoder(JSONEncoder):
    """ Custom Json encoder to handle timedelta """

    # pylint: disable=E0202
    def default(self, obj):
        if isinstance(obj, datetime.timedelta):
            minutes, seconds = divmod(obj.total_seconds(), 60)
            hours, minutes = divmod(minutes, 60)
            return "%02d:%02d:%02d" % (hours, minutes, seconds)

        return JSONEncoder.default(self, obj)

