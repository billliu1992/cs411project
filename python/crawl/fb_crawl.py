from fbutil import FacebookUtil

print("HELLO")

eventId = FacebookUtil.url_get_event_id("https://www.facebook.com/events/459429424189382/?ref_dashboard_filter=upcoming")

print("Got event id: " + eventId)

got_back = FacebookUtil.get_event_dict(eventId)

print("Got back: " + str(got_back))
