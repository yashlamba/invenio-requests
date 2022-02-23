// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import {
  InvenioRequestsAPI,
  RequestLinkExtractor,
  InvenioRequestEventsApi,
  RequestEventsLinkExtractor,
} from "./api/api";
import {
  Request
} from './request';
import React, { Component } from "react";
import PropTypes from "prop-types";
import { configureStore } from "./store";
import { OverridableContext } from "react-overridable";
import { Provider } from "react-redux";

export class InvenioRequestsApp extends Component {
  constructor(props) {
    super(props);
    const { requestsApi, requestEventsApi, request } = this.props;
    const defaultRequestsApi = new InvenioRequestsAPI(
      new RequestLinkExtractor(request)
    );
    const defaultRequestEventsApi = (commentLinks) =>
      new InvenioRequestEventsApi(new RequestEventsLinkExtractor(commentLinks));

    const appConfig = {
      requestsApi: requestsApi || defaultRequestsApi,
      request,
      requestEventsApi: requestEventsApi || defaultRequestEventsApi,
      refreshIntervalMs: 5000,
    };

    this.store = configureStore(appConfig);
  }

  render() {
    const { overriddenCmps } = this.props;
    return (
      <OverridableContext.Provider value={overriddenCmps}>
        <Provider store={this.store}>
          <Request />
        </Provider>
      </OverridableContext.Provider>
    );
  }
}

InvenioRequestsApp.propTypes = {
  requestsApi: PropTypes.object,
  requestEventsApi: PropTypes.object,
  overriddenCmps: PropTypes.object,
  request: PropTypes.object.isRequired,
};

InvenioRequestsApp.defaultProps = {
  overriddenCmps: {},
  requestsApi: null,
};