# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# User specific environment and startup programs

# User specific environment and startup programs

#PATH=$PATH:$HOME/.local/bin:$HOME/bin

export PATH=/usr/local/cuda/bin:/usr/local/MATLAB/R2017b/bin:/usr/local/openmpi-1.10.2/bin/:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/openmpi-1.10.2/lib

source /opt/intel/bin/compilervars.sh -arch intel64

export MKL_THREADING_LAYER=GNU

export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.161-0.b14.el7_4.x86_64
export PATH=${JAVA_HOME}/bin:/opt/hadoop/bin:${PATH}
export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
export MKL_THREADING_LAYER=GNU
