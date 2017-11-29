# remove subdirectories
# rm -R -- */

for i in ./data/*.zip;do
        fbname=$(basename "$i" .zip)
        # mkdir $fbname
        unzip $i  -d uncompress-data/$fbname ;
done