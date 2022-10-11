all
# our changelog does this, by design
# exclude_rule 'MD003'
# rule 'MD007', :indent => 3
rule 'MD013', :heading_line_length => 90
# => doesn't work for style
# rule 'MD029', :style => :ordered
rule "MD029", style: "ordered"
