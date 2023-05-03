#!/bin/bash

input_dir=$1

for idx in {1..5}
do
  output_dir="rslt025_${input_dir}${idx}"
  script="$input_dir${idx}.sh"
  param_file="$input_dir${idx}.param.in"
  submit_file="$input_dir${idx}.submit"

  if [[ ! -d "$output_dir" ]]; then
    mkdir $output_dir
  fi 
  
  printf "" > $param_file
  let cnt=0
  n_files=`ls -1q $input_dir/[0-9]*.txt | wc -l`
  # generate params
  for id in $(seq 0 $n_files) 
  # file in $input_dir/*
  do
    # echo $file
    cnt=$((cnt+1))
    # id=$(sed 's/.*\/\(.*\)\..*/\1/' <<< "$file")
    printf "$id.txt" >> $param_file
    # printf "\t$output_dir/$id.txt\n" >> $param_file
    printf "\t${id}out.txt\n" >> $param_file
  done

  # write script to be run
  printf "#!/bin/bash\n" > $script
  echo 'i=$1' >> $script
  echo 'i=$((i+1))' >> $script
  echo 'x=$(sed "${i}q;d"' $param_file "| awk '{print \$1}')" >> $script
  echo 'y=$(sed "${i}q;d"' $param_file "| awk '{print \$2}')" >> $script
  echo "dist=binom" >> $script
  echo './gph $x $y 100000 $dist 0.25 0.0 0.01 0.02 0.03 0.05 0.07 0.08 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9' >> $script
  chmod +x $script

  # write the submit file
  echo "Universe = vanilla" > $submit_file
  echo "Executable = $script" >> $submit_file
  echo 'Arguments = $(process)' >> $submit_file

  echo 'Error = log/osgJob$(process).err' >> $submit_file
  echo "Output = $output_dir/"'$(process).out' >> $submit_file
  echo 'Log = log/osgJob$(process).log' >> $submit_file

  echo "should_transfer_files = YES" >> $submit_file
  echo "when_to_transfer_output = ON_EXIT" >> $submit_file
  echo "transfer_input_files=gph, $input_dir/\$(process).txt, $param_file" >> $submit_file
  # echo "transfer_output_files=$output_dir/" >> $submit_file
  echo "transfer_output_remaps = \"\$(process)out.txt=$output_dir/\$(process)out.txt\"" >> $submit_file
  echo "request_memory = 2GB" >> $submit_file
  echo "Queue $cnt" >> $submit_file

  condor_submit $submit_file
done
#
