--[[
  Lua filter to add draft watermark to PDF output when draft: true

  This filter checks the document metadata for draft: true and automatically
  injects a LaTeX watermark package to add "DRAFT" to every page of the PDF.

  This mirrors the automatic draft banner behavior in HTML output.
]]--

function Meta(meta)
  -- Only process for PDF output
  if quarto.doc.isFormat("pdf") then
    -- Check if draft metadata is set to true
    if meta.draft == true then
      -- Add LaTeX packages and watermark configuration
      local header = [[
\usepackage{draftwatermark}
\SetWatermarkText{DRAFT}
\SetWatermarkScale{1.5}
\SetWatermarkColor[gray]{0.85}
\SetWatermarkAngle{55}
]]

      -- Inject into header-includes
      if meta['header-includes'] then
        -- Append to existing header-includes
        table.insert(meta['header-includes'], pandoc.RawBlock('latex', header))
      else
        -- Create new header-includes
        meta['header-includes'] = pandoc.MetaList{pandoc.RawBlock('latex', header)}
      end

      quarto.log.output("Draft mode enabled - adding watermark to PDF")
    end
  end

  return meta
end
