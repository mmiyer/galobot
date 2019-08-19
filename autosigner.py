from botbase import *
from pywikibot.comms.eventstreams import EventStreams  # pylint: disable=import-error


def sign_diff(old_id, new_id):
    """
    Creates diff based on revisions and determines based on diff whether
	something needs to be signed, and where to insert sign
    """


# in reality, all namespaces except for main are valid
# need to check category to find wikipedia space pages that need signing
valid_namespaces = (1, 3, 5, 7, 9, 11, 13, 15, 101, 109, 119, 711, 829, 2301, 2303)
stream = EventStreams(streams="recentchange")
stream.register_filter(
    type="edit", wiki="enwiki", bot=False, namespace=valid_namespaces
)

for edit in stream:
    print(edit)
