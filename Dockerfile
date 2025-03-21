FROM ros:jazzy

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

WORKDIR /ros2_ws

# Dependencies
RUN apt-get update 
RUN apt-get install -y \
    python3-rosdep \
    python3-rosinstall-generator \
    python3-colcon-common-extensions \
    build-essential \
    tmux \
    git \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Initialize rosdep if not already initialized
RUN rosdep init || echo "rosdep already initialized" && rosdep update

# Create ROS 2 workspace
RUN mkdir -p /ros2_ws/src

# Uncomment when we have packages
# COPY ./package_dir /ros2_ws/src/package_dir

# Install package dependencies
# RUN cd /ros2_ws && rosdep install --from-paths src --ignore-src -r -y

# Build the workspace
RUN source /opt/ros/jazzy/setup.bash \
    && cd /ros2_ws \
    && colcon build

# Add workspace setup to bashrc
RUN echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc 

# Set up the entrypoint
COPY ./ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]

CMD ["bash"]

RUN echo "All Done"