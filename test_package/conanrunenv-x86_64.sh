script_folder="/home/ecku/develop/recipes/conan-cuda_dev_config/test_package"
echo "echo Restoring environment" > "$script_folder/deactivate_conanrunenv-x86_64.sh"
for v in PATH LD_LIBRARY_PATH DYLD_LIBRARY_PATH
do
   is_defined="true"
   value=$(printenv $v) || is_defined="" || true
   if [ -n "$value" ] || [ -n "$is_defined" ]
   then
       echo export "$v='$value'" >> "$script_folder/deactivate_conanrunenv-x86_64.sh"
   else
       echo unset $v >> "$script_folder/deactivate_conanrunenv-x86_64.sh"
   fi
done

export PATH="/usr/local/cuda-13.0/bin${PATH:+:$PATH}"
export LD_LIBRARY_PATH="/usr/local/cuda-13.0/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export DYLD_LIBRARY_PATH="/usr/local/cuda-13.0/lib64${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"