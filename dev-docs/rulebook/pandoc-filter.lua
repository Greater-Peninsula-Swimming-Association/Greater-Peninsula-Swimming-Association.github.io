-- pandoc-filter.lua
-- This filter instructs pandoc to treat code blocks with the class 'latex'
-- as raw LaTeX output. This allows embedding LaTeX commands in Markdown
-- that can be hidden by CSS in mkdocs, but processed by pandoc for PDF output.

function CodeBlock(el)
  if el.classes:includes('latex') then
    return pandoc.RawBlock('latex', el.text)
  end
end
