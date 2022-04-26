local clickable = {}
clickable.buttons = {}

function clickable.createButton(x, y, graphic, mode)
    o = {}
    o.x = x
    o.y = y
    o.xw = graphic:getHeight()
    o.yw = graphic:getWidth()
    o.graphic = graphic
    o.mode = mode
    table.insert(clickable.buttons, o)
end


function clickable.checkButtons(mouseX, mouseY)
    -- returns button if button was clicked on this frame (otherwise, nil)
    for i,button in ipairs(clickable.buttons) do
        if (mouseX > button.x and mouseX < (button.x + button.xw)) and (mouseY > button.y and mouseY < (button.y + button.yw)) then
            return button
        end
    end
    return nil
end

return clickable