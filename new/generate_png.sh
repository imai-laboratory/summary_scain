for i in `seq 9 `
do
    for j in `seq 0 7`
    do
	tex2img --top-margin 100 --left-margin 100 --right-margin 100 --bottom-margin 100 --no-transparent ./data/00${i}_00${j}full.tex ./png/00${i}_00${j}full.png
    done
done

for i in `seq 9 `
do
    for j in `seq 0 7`
    do
	tex2img --top-margin 100 --left-margin 100 --right-margin 100 --bottom-margin 100 --no-transparent ./data/00${i}_00${j}omitted.tex ./png/00${i}_00${j}omitted.png
    done
done

for j in `seq 0 7`
do
tex2img --top-margin 100 --left-margin 100 --right-margin 100 --bottom-margin 100 --no-transparent ./data/010_00${j}full.tex ./png/010_00${j}full.png
done

for j in `seq 0 7`
do
tex2img --top-margin 100 --left-margin 100 --right-margin 100 --bottom-margin 100 --no-transparent ./data/010_00${j}omitted.tex ./png/010_00${j}omitted.png
done


# tex2img --top-margin 100 --left-margin 100 --right-margin 100 --bottom-margin 100 --no-transparent ./data/003_004full.tex ./png/003_004full.png
# tex2img --top-margin 100 --left-margin 100 --right-margin 100 --bottom-margin 100 --no-transparent ./data/003_004omitted.tex ./png/003_004omitted.png

