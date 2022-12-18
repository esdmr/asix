#!/usr/bin/env fish

# This file generates a graph of all python imports. Previously I used this to
# find and resolve circular dependencies. Now it just generates a colorful arrow
# spaghetti.
#
# You'll need fish shell and Graphviz (dot) to run this script.

if not type -q dot
    echo 'Graphviz (dot) executable not in PATH.' >&2
    exit 1
end

set seed_file (mktemp --suffix .txt)
set dot_file (mktemp --suffix .dot)
set svg_file (mktemp --suffix .svg)

echo 'digraph G {

node [fontname="Fira Code"]' >$dot_file

function pythonify
    string replace / . -- $argv | string replace .__init__ '' | string replace -r '\b\w+\.\.' ''
end

for line in (rg '(?:import|from) (?:asix)?(?:\.[\w.]|\s)' asix/)
    string match -qr '^asix/(?<path>(?<dir>(?:\w+/)*)\w+)\.py:(?<space>\s*)(?:from|import)\s+(?<is_absolute>asix)?(?:\.(?<what>[\w.]+)|\s)' -- $line
    or begin
        echo $line >&2
        continue
    end

    # printf '// %s\n' $line >>$dot_file

    if test -z "$what"
        set what __init__
    end

    if test -z "$is_absolute" -a -n "$dir"
        set what $dir$what
    end

    set what (pythonify $what)
    set path (pythonify $path)
    set style ''

    if test -n "$space"
        set style ' [style=dashed,arrowhead=vee,constraint=false,color=gray]'
        continue
    else
        set style ' [color="#'(echo $path $what | sha1sum | string sub -l 6)'"]'
    end

    printf '"%s" -> "%s"%s\n' $path $what $style >>$dot_file
end

echo '
}' >>$dot_file
dot -Tsvg $dot_file >$svg_file
cat $dot_file | nop
rm $dot_file

if type -q eog
    eog $svg_file
    rm $svg_file
end
