# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Base class for creating custom types of requests.

The `RequestType` classes are the most important part in the customization/extension
mechanism for custom types of requests.
TODO explain what can be done here, and how!
"""


from uuid import uuid4


class RequestType:
    """Base class for custom request types."""

    type_id = "invenio-requests.request"
    """The unique and constant identifier for this type of requests.

    Since this property is used to map generic chunks of data from the database
    (i.e. the request model entries) to their correct `RequestType`, this should
    be a globally unique value.
    By convention, this would be the name of the package in which the custom
    `RequestType` is defined as prefix, together with a suffix related to the
    `RequestType`.
    Further, it should be constant after the first release of the package
    (otherwise, requests created with the old value will no longer be able to be
    mapped to their `RequestType`).
    """

    name = "Generic Request"
    """The human-readable name for this type of requests."""

    available_statuses = {
        "draft": True,
        "open": True,
        "cancelled": False,
        "declined": False,
        "accepted": False,
        "expired": False,
    }
    """Available statuses for the Request.

    The keys in this dictionary is the set of available statuses, and their
    values are indicators whether this Request is still considered to be
    "open" in this state.
    """

    available_actions = {}
    """Available actions for this Request.

    The keys are the internal identifiers for the actions, the values are
    the actual RequestAction classes (not objects).
    Whenever an action is looked up, a new object of the registered
    RequestAction class is instantiated with the current Request object as
    argument.
    """

    marshmallow_schema = None
    """Schema used for de/serialization of requests of this type.

    To be overridden in subclasses, if the custom request type follows a
    different or more specific schema.
    """

    creator_can_be_none = True
    """Determines if the ``created_by`` reference accepts ``None``."""

    receiver_can_be_none = False
    """Determines if the ``receiver`` reference accepts ``None``."""

    topic_can_be_none = True
    """Determines if the ``topic`` reference accepts ``None``."""

    allowed_creator_ref_types = ["user"]
    """A list of allowed TYPE keys for ``created_by`` reference dicts."""

    allowed_receiver_ref_types = ["user"]
    """A list of allowed TYPE keys for ``receiver`` reference dicts."""

    allowed_topic_ref_types = []
    """A list of allowed TYPE keys for ``topic`` reference dicts."""

    def generate_external_id(self, request, **kwargs):
        """Generate a new external identifier.

        This method can be overridden in subclasses to create external identifiers
        according to a custom schema, using the information associated with the request
        (e.g. topic, receiver, creator).
        """
        return str(uuid4())

    def __str__(self):
        """Return str(self)."""
        return self.name

    def __repr__(self):
        """Return repr(self)."""
        return f"<RequestType '{self.name}'>"