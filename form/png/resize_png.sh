for f in *.png
do 
    convert -crop 3730x2200+0+0 ${f} ../resized/${f}
done
