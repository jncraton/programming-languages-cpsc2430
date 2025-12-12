SHELL := bash -O nullglob

all: index.html syllabus.md syllabus.html syllabus.docx syllabus.txt syllabus.pdf env.html lectures/index.html examples/index.html

.PHONY: clean lectures

syllabus.md: syllabus-template.md head.md tail.md
	cp -f $< $@
	sed -i -e "/head.md/{r head.md" -e "d}" $@
	sed -i -e "/tail.md/{r tail.md" -e "d}" $@

readme.md: syllabus.md
	cp -f $< $@

syllabus.txt: syllabus.md
	cp syllabus.md syllabus.txt

syllabus.html: syllabus.md
	pandoc -V lang=en --metadata pagetitle=Syllabus --standalone --css=style.css --lua-filter=filters.lua -o $@ $<

index.html: syllabus.html
	cp -f $< $@

syllabus.docx: syllabus.md
	pandoc -V lang=en --metadata pagetitle=Syllabus --reference-doc reference.docx -o $@ $<

syllabus.pdf: syllabus.md
	pandoc -V lang=en --metadata title-meta=Syllabus --variable documentclass=article --variable fontsize=12pt --variable mainfont="FreeSans" --variable mathfont="FreeMono" --variable monofont="FreeMono" --variable monofontoptions="SizeFeatures={Size=8}" --include-in-head head.tex --no-highlight -V 'hyphens=none' --mathjax=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js --variable titlepage="false" -s -o $@ $<
	gs					\
		-q -dNOPAUSE -dBATCH -dSAFER		\
		-sDEVICE=pdfwrite			\
		-dCompatibilityLevel=1.4		\
		-dPDFSETTINGS=/screen			\
		-dEmbedAllFonts=true			\
		-dSubsetFonts=true			\
		-dCompressFonts=true \
		-dAutoRotatePages=/None		\
		-dColorImageDownsampleType=/Bicubic	\
		-dColorImageResolution=75		\
		-dGrayImageDownsampleType=/Bicubic	\
		-dGrayImageResolution=75		\
		-dMonoImageDownsampleType=/Bicubic	\
		-dMonoImageResolution=75		\
		-sOutputFile=syllabus-comp.pdf \
		syllabus.pdf
	mv -f syllabus-comp.pdf syllabus.pdf
	cp syllabus.pdf $(shell basename $(CURDIR)).pdf

env.html: env.md
	pandoc -V lang=en --metadata pagetitle=Environment --standalone --css=style.css -o $@ $<

lectures:
	find lectures -name "*.md" -exec pandoc --mathjax=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js -t revealjs --standalone --template=revealjs-template.html -V revealjs-url=reveal.js -V theme:white -V history=true --metadata pagetitle=Slides -o "{}.html" "{}" \;
	for file in lectures/*.md.html; do \
	    mv -- "$$file" "$$(echo $$file | sed 's/.md//')"; \
	done
	for file in lectures/media/*.puml; do \
	    plantuml -Sdpi=300 -output .. "$$file"; \
	done

spellcheck:
	aspell --home-dir=. --check --dont-backup head.md
	aspell --home-dir=. --check --dont-backup readme.md
	aspell --home-dir=. --check --dont-backup tail.md
	aspell --home-dir=. --check --dont-backup env.md
	for f in lectures/*.md; do aspell --home-dir=. --check --dont-backup "$$f"; done

lectures/all.md:
	rm -f lectures/all.md # This must be deleted, or it will be included in itself and hang the build
	cd lectures && sed -e '$$G' -s `ls -v *.md` > all.md

lectures/all.html: lectures/all.md
	pandoc -V lang=en --metadata pagetitle="Lecture Notes" --standalone --mathjax=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js --css=../style.css -o $@ $<

lectures/all-slides.html: lectures/all.md
	pandoc --mathjax=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js -t revealjs --standalone --template=revealjs-template.html -V revealjs-url=reveal.js -V theme:white -V history=true --metadata pagetitle=Slides -o $@ $<

lectures/index.html: lectures lectures/all.html lectures/all-slides.html lectures/reveal.js
	python3 gen_lecture_index.py
	pandoc lectures/index.md -o $@

examples/index.html:
	cd examples && tree -H '.' -L 2 --noreport --charset utf-8 -P "*" | sponge index.html

lectures/reveal.js:
	cd lectures && git clone --depth=1 --branch 5.2.0 https://github.com/hakimel/reveal.js

update:
	wget -q -N https://raw.githubusercontent.com/jncraton/course-template/master/.gitignore \
	           https://raw.githubusercontent.com/jncraton/course-template/master/head.tex \
	           https://raw.githubusercontent.com/jncraton/course-template/master/makefile \
	           https://raw.githubusercontent.com/jncraton/course-template/master/reference.docx \
	           https://raw.githubusercontent.com/jncraton/course-template/master/requirements.txt \
	           https://raw.githubusercontent.com/jncraton/course-template/master/runtime.md \
	           https://raw.githubusercontent.com/jncraton/course-template/master/head.md \
	           https://raw.githubusercontent.com/jncraton/course-template/master/tail.md \
	           https://raw.githubusercontent.com/jncraton/course-template/master/env.md \
	           https://raw.githubusercontent.com/jncraton/course-template/master/style.css \
	           https://raw.githubusercontent.com/jncraton/course-template/master/filters.lua \
	           https://raw.githubusercontent.com/jncraton/course-template/master/revealjs-template.html \
	           https://raw.githubusercontent.com/jncraton/course-template/master/gen_dates.py \
	           https://raw.githubusercontent.com/jncraton/course-template/master/gen_lecture_index.py \
	           https://raw.githubusercontent.com/jncraton/course-template/master/config.json

	mkdir -p .github/workflows
	cd .github/workflows && wget -q -N https://raw.githubusercontent.com/jncraton/course-template/master/.github/workflows/pages.yml

	# readme.md was previously used as syllabus template
	# Copy it if needed when updating
	cp --no-clobber readme.md syllabus-template.md
	git add -f syllabus-template.md

	git add -f gen_lecture_index.py

	make readme.md

clean:
	rm -rf pandoc*
	rm -f index.html index.md syllabus.md syllabus.docx syllabus.html syllabus.pdf env.html *.pdf
	rm -rf lectures/**.html lectures/all.md lectures/index.md
	rm -rf lectures/*.png
	rm -rf examples/index.html
	find lectures -name "*.html" -exec rm -f {} \;
	rm -rf figures
	rm -rf __pycache__
	rm -f netlifyctl
	rm -rf revealjs
	rm -rf lectures/reveal.js
	rm -f readme-template.md
