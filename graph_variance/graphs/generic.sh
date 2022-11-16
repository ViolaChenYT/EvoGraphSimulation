#!/bin/bash

input_dir=$1

for idx in {1..5}
do
  output_dir="res_s0_${input_dir}${idx}"
  script="$input_dir${idx}.sh"
  param_file="$input_dir${idx}.param.in"
  submit_file="$input_dir${idx}.submit"

  if [[ ! -d "$output_dir" ]]; then
    mkdir $output_dir
  fi 
  
  printf "" >> $param_file
  let cnt=0
  # generate params
  for file in $input_dir/*
  do
    # echo $file
    cnt=$((cnt+1))
    id=$(sed 's/.*\/\(.*\)\..*/\1/' <<< "$file")
    printf $file >> $param_file
    printf "\t$output_dir/$id.txt\n" >> $param_file
  done

  # write script to be run
  printf "#!/bin/bash\n" > $script
  echo 'i=$1' >> $script
  echo 'i=$((i+1))' >> $script
  echo 'x=$(sed "${i}q;d"' $param_file "| awk '{print \$1}')" >> $script
  echo 'y=$(sed "${i}q;d"' $param_file "| awk '{print \$2}')" >> $script
  echo "dist=binom" >> $script
  echo './gph.out $x $y 10000 $dist 0.0 0.0 0.9' >> $script
  chmod +x $script

  # write the submit file
  echo "Universe = vanilla" > $submit_file
  echo "Executable = $script" >> $submit_file
  echo 'Arguments = $(process)' >> $submit_file

  echo 'Error = log/osgJob$(process).err' >> $submit_file
  echo 'Output = log/osgJob$(process).out' >> $submit_file
  echo 'Log = log/osgJob$(process).log' >> $submit_file

  echo "should_transfer_files = YES" >> $submit_file
  echo "when_to_transfer_output = ON_EXIT" >> $submit_file
  echo "transfer_input_files=gph.out, $input_dir, $param_file, $output_dir" >> $submit_file
  echo "transfer_output_files=$output_dir" >> $submit_file
  echo "request_memory = 2GB" >> $submit_file
  echo "Queue $cnt" >> $submit_file

  condor_submit $submit_file
done
#
