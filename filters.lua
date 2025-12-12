function Link(element)
    -- Force all links to open in the full body of the window
    -- Prevents issue when linking to lecture slides from within iframes
    if 
        string.sub(element.target, 1, 1) ~= "#"
    then
        element.attributes.target = "_top"
    end
    return element
end
