#!/bin/bash

input_dir=$1
output_dir=$2

script="$input_dir.sh"
param_file="$input_dir.param.in"
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

# write script to be ran
printf "#!/bin/bash\n" > $script
echo 'i=$1' >> $script
echo "i=$((i+1))" >> $script
echo 'x=$(sed "${i}q;d"' $param_file "| awk '{print \$1}')" >> $script
echo 'y=$(sed "${i}q;d"' $param_file "| awk '{print \$2}')" >> $script
echo "dist=binom" >> $script
echo './gph.out $x $y 50000 $dist 0.1 0.0 0.9' >> $script
chmod +x $script

# write the submit file
submit_file="$input_dir.submit"
echo "Universe = vanilla" > $submit_file
echo "Executable = $script" >> $submit_file
echo 'Arguments = $(process)' >> $submit_file

echo 'Error = log/osgJob$(process).err' >> $submit_file
echo 'Output = log/osgJob$(process).out' >> $submit_file
echo 'Log = log/osgJob$(process).log' >> $submit_file

echo "should_transfer_files = YES" >> $submit_file
echo "when_to_transfer_output = ON_EXIT" >> $submit_file
echo "gph.out, $input_dir, $param_file, $output_dir" >> $submit_file
echo "transfer_output_files=$output_dir" >> $submit_file

echo "Queue $cnt" >> $submit_file
#