FROM ctumrs/mrs_uav_system:1.5.0

ARG BUILD_PATH="/tmp/build"
ARG HAILORT_VERSION="v4.18.0"

RUN apt install -y ros-noetic-vision-msgs libopencv-dev python3-opencv

# build required hailort driver
RUN mkdir -p ${BUILD_PATH}
RUN cd ${BUILD_PATH} && \
  git clone https://github.com/hailo-ai/hailort.git && \
  cd hailort && \
  git checkout ${HAILORT_VERSION} && \
  cd ${BUILD_PATH}/hailort && \
  cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release -DHAILO_BUILD_EXAMPLES=0 && \
  sudo cmake --build build --config release --target install && \
  rm -rf ${BUILD_PATH}

CMD ["/ros_entrypoint.sh"]
