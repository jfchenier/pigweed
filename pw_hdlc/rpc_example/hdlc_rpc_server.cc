// Copyright 2020 The Pigweed Authors
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License. You may obtain a copy of
// the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations under
// the License.

#include <array>
#include <string_view>

#include "pw_assert/check.h"
#include "pw_hdlc/encoder.h"
#include "pw_hdlc/rpc_packets.h"
#include "pw_log/log.h"
#include "pw_rpc/echo_service_nanopb.h"
#include "pw_rpc/server.h"
#include "pw_rpc_system_server/rpc_server.h"
#include "pw_span/span.h"

namespace pw::rpc {
constexpr char outputStr[] =
    "%dHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHelloWorldHe"
    "lloWorldHelloWorldHelloWorld";
}

namespace hdlc_example {
namespace {

pw::rpc::ByteService echo_service;

void RegisterServices() {
  pw::rpc::system_server::Server().RegisterService(echo_service);
}

}  // namespace

void Start() {
  pw::rpc::system_server::Init();

  // Set up the server and start processing data.
  RegisterServices();

  PW_LOG_INFO("Starting pw_rpc server");
  PW_CHECK_OK(pw::rpc::system_server::Start());
}

}  // namespace hdlc_example

namespace pw::rpc {

class ByteWriter {
 public:
  ByteWriter(ByteService::ServerWriter<pw_rpc_ByteMessage>& response_writer)
      : response_(pw_rpc_ByteMessage_init_zero),
        response_writer_(response_writer) {}

  void Write(const int i) {
    response_.msg.size = std::snprintf(
        (char*)response_.msg.bytes, sizeof(response_.msg.bytes), outputStr, i);

    response_writer_.Write(response_);
  }

  void Flush() {
    response_ = pw_rpc_ByteMessage_init_zero;
    response_writer_.Finish();
  }

 private:
  pw_rpc_ByteMessage response_;
  // This RPC stream writer handle must be valid for the metric writer lifetime.
  ByteService::ServerWriter<::pw_rpc_ByteMessage>& response_writer_;
};

// Method definitions for pw.rpc.ByteService.
void ByteService::Send(
    ServerReader<::pw_rpc_ByteMessage, ::pw_rpc_ByteStatus>& reader) {
  reader_ = std::move(reader);

  reader_.set_on_next([this](const pw_rpc_ByteMessage ByteMessage) {
    static int i;

    // TODO: Read the request as appropriate for your application
    static_cast<void>(ByteMessage);

    /* Send the message 1000 times before finishing the stream */
    if (i++ > 500) {
      pw_rpc_ByteStatus byteStatus;
      byteStatus.status = 1;
      i = 0;
      reader_.Finish(byteStatus);
    }
  });
}

void ByteService::Receive(const ::pw_rpc_ByteStatus& request,
                          ServerWriter<::pw_rpc_ByteMessage>& writer) {
  // TODO: Read the request as appropriate for your application
  static_cast<void>(request);
  volatile int j;
  // TODO: Send responses with the writer as appropriate for your
  // application
  ByteWriter byte_writer(writer);

  for (uint32_t i = 0; i < request.status; i++) {
    byte_writer.Write(i);

    // Empty loop to create delay
    for (j = 0; j < 10000; j++) {
    }
  }
  byte_writer.Flush();
}

}  // namespace pw::rpc
