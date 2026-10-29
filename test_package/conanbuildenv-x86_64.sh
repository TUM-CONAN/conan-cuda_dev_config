script_folder="/home/ecku/develop/recipes/conan-cuda_dev_config/test_package"
echo "echo Restoring environment" > "$script_folder/deactivate_conanbuildenv-x86_64.sh"
for v in PATH CUDA_SDK_ROOT_DIR CUDAARCHS
do
   is_defined="true"
   value=$(printenv $v) || is_defined="" || true
   if [ -n "$value" ] || [ -n "$is_defined" ]
   then
       echo export "$v='$value'" >> "$script_folder/deactivate_conanbuildenv-x86_64.sh"
   else
       echo unset $v >> "$script_folder/deactivate_conanbuildenv-x86_64.sh"
   fi
done

export PATH="${PATH:-}${PATH:+:}/usr/local/cuda-13.0/lib64:/usr/local/cuda-13.0/bin"
export CUDA_SDK_ROOT_DIR="/usr/local/cuda-13.0"
export CUDAARCHS="86;120"