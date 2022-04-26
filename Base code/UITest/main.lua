controller = require "controller"
clickable = require "clickable"
constraint = require "constraint"

viewingMode = 1 -- 1 for single, 2 for connected
drawingMode = 1 -- 1 for line, 2 for curve
mouse = {}
mouse.justDown = false

curves = {}
bezQueue = {}
lineQueue = {}
arcQueue = {}
lastInsert = ""

errorConsole = ""

layerData = {}

function newCurve(type)
    o = {}
    o.type = type
    o.pts = {}
    return o
end

function newLayer(index)

    o = {}
    o.index = index
    o.pts = {}
    
    table.insert(layerData, o)

end

function getLayerPoints(index)
    for i=1,#layerData do
        if layerData[i].index == index then
            return layerData[i].pts
        end
    end
    return nil
end

newLayer(0)
layer = 0
points = getLayerPoints(0)
pointsTransLower = {}
pointsTransUpper = {}

function love.load()

    love.window.setTitle("CurveTool")

    love.graphics.setLineWidth(2)

    help_ico = love.graphics.newImage("help.png")
    rhombus = love.graphics.newImage("p_rhombus.png")
    grid = love.graphics.newImage("protogrid.png")
    curve = love.graphics.newImage("curve.png")
    line = love.graphics.newImage("line.png")
    arc = love.graphics.newImage("arc.png")
    save = love.graphics.newImage("img.png")

    controller.initButtons()

    clickable.createButton(0, 0, line, 1)
    clickable.createButton(20, 0, curve, 2)
    clickable.createButton(40, 0, arc, 3)
    clickable.createButton(768, 0, save, 10)
    

    font = love.graphics.newFont("roman.ttf", 28)
    fontTiny = love.graphics.newFont("roman.ttf", 14)
    love.graphics.setFont(font)

    canvas = love.graphics.newCanvas()
    love.graphics.setCanvas(canvas)
    love.graphics.rectangle("fill", 0, 0, 800, 600)
    love.graphics.setCanvas()

    lineCanvas = love.graphics.newCanvas()
end

function snapPoint(x, y, kind)
    -- coordinate origin is 46, 50

    -- first: clamp x and y

    x = math.max(x, 46)
    x = math.min(x, 746)
    y = math.max(y, 46)
    y = math.min(y, 546)

    -- next: round to nearest point
    
    x = math.floor((x - ((x - 46) % 20)) + 0.5)
    y = math.floor((y - ((y - 46) % 20)) + 0.5)

    realx = (x - 46) / 20
    realy = (y - 46) / 20

    -- returned value is in the form (screencoordX, screencoordY, localcoordX, localcoordY, type)
    o = {}
    o.x = x
    o.y = y
    o.realx = realx
    o.realy = realy
    o.kind = kind

    return o

end

function updateQueues(newPoint)
    errorConsole = ""
    if newPoint.kind == "line" then
        
        lastInsert = "line"
        

        -- adjust other queues
        bezQueue = {snapPoint(newPoint.x, newPoint.y, "bez")}
        arcQueue = {snapPoint(newPoint.x, newPoint.y, "arc")}

        if #lineQueue == 1  then
            if constraint.checkG1(lineQueue[1], newPoint, points[#points - 1], points[#points]) then
                table.insert(points, lineQueue[1])
                table.insert(points, newPoint)
                lineQueue = {newPoint}
            else
                errorConsole = "ERROR: Curve not G1 continuous"
                bezQueue = {snapPoint(points[#points].x, points[#points].y, "bez")}
                lineQueue = {snapPoint(points[#points].x, points[#points].y, "line")}
                arcQueue = {snapPoint(points[#points].x, points[#points].y, "arc")}
            end
            lastInsert = "none"
        else
            table.insert(lineQueue, newPoint)
        end

    elseif newPoint.kind == "bez" then

        lastInsert = "bez"

        --print("Length of bezQueue is " .. #bezQueue)

        -- adjust other queues
        lineQueue = {snapPoint(newPoint.x, newPoint.y, "line")}
        arcQueue = {snapPoint(newPoint.x, newPoint.y, "arc")}

        if #bezQueue == 3  then
            if (constraint.checkG1(bezQueue[1], bezQueue[2], points[#points - 1], points[#points])) then
                table.insert(points, bezQueue[1])
                table.insert(points, bezQueue[2])
                table.insert(points, bezQueue[3])
                table.insert(points, newPoint)
                bezQueue = {snapPoint(newPoint.x, newPoint.y, "bez")}
            else 
                errorConsole = "ERROR: Curve not G1 continuous"
                bezQueue = {snapPoint(points[#points].x, points[#points].y, "bez")}
                lineQueue = {snapPoint(points[#points].x, points[#points].y, "line")}
                arcQueue = {snapPoint(points[#points].x, points[#points].y, "arc")}
            end
            lastInsert = "none"
        else
            table.insert(bezQueue, newPoint)
        end

    elseif newPoint.kind ==  "arc" then


    end
end

function love.update(dt)

    controller.updateKeys()
    checkMouse()
    if (mouse.justDown) then

        mouseX, mouseY = love.mouse.getPosition()

        buttonPressed = clickable.checkButtons(mouseX, mouseY)

        if not (buttonPressed == nil) then
            if buttonPressed.mode < 10 then
                drawingMode = buttonPressed.mode
            elseif buttonPressed.mode == 10 then
                -- save
                lineCanvas:newImageData():encode("png", "out.png")
            end
        else

            if drawingMode == 1 then
                kind = "line"
            elseif drawingMode == 2 then
                kind = "bez"
            elseif drawingMode == 3 then
                kind = "arc"
            end

            pointTemp = snapPoint(mouseX, mouseY, kind)

            updateQueues(pointTemp)

        end

    end

    if (controller.keys.up.JustPressed) then
        new_pts = getLayerPoints(layer + 1)
        if new_pts == nil then
            -- create new layer
            newLayer(layer + 1)
            points = getLayerPoints(layer + 1)
        else
            points = new_pts
        end
        layer = layer + 1
    end

    if (controller.keys.down.JustPressed) then
        new_pts = getLayerPoints(layer - 1)
        if new_pts == nil then
            -- create new layer
            newLayer(layer - 1)
            points = getLayerPoints(layer - 1)
        else
            points = new_pts
        end
        layer = layer - 1
    end

    if (controller.keys.a.JustPressed) then
        if viewingMode == 1 then
            -- generate set of transformed points
            viewingMode = 2
        else
            viewingMode = 1
        end

    end

    if (controller.keys.z.JustPressed) then
        -- undo
        errorConsole = ""
        if viewingMode == 1 then
            if lastInsert == "none" then
                if #points > 0 and points[#points].kind == "line" then
                    table.remove(points)
                    table.remove(points)
                    if #points > 0 then
                        lineQueue = {snapPoint(points[#points].x, points[#points].y, "line")}
                        bezQueue = {snapPoint(points[#points].x, points[#points].y, "bez")}
                        arcQueue = {snapPoint(points[#points].x, points[#points].y, "arc")}
                    else
                        lineQueue = {}
                        bezQueue = {}
                        arcQueue = {}
                    end
                    lastInsert = "none"
                elseif #points > 0 and points[#points].kind == "bez" then
                    table.remove(points)
                    table.remove(points)
                    table.remove(points)
                    table.remove(points)
                    if #points > 0 then
                        lineQueue = {snapPoint(points[#points].x, points[#points].y, "line")}
                        bezQueue = {snapPoint(points[#points].x, points[#points].y, "bez")}
                        arcQueue = {snapPoint(points[#points].x, points[#points].y, "arc")}
                    else
                        lineQueue = {}
                        bezQueue = {}
                        arcQueue = {}
                    end
                    lastInsert = "none"
                else
                    errorConsole = "ERROR: Nothing to undo!"
                end
            else
                if #points > 0 then
                    lineQueue = {snapPoint(points[#points].x, points[#points].y, "line")}
                    bezQueue = {snapPoint(points[#points].x, points[#points].y, "bez")}
                    arcQueue = {snapPoint(points[#points].x, points[#points].y, "arc")}
                    lastInsert = "none"
                else
                    errorConsole = "ERROR: Nothing to undo!"
                end
            end
        end
    end

end

function love.draw()

    love.graphics.draw(canvas, 0, 0)

    for _,button in ipairs(clickable.buttons) do
        love.graphics.draw(button.graphic, button.x, button.y)
    end

    love.graphics.setColor(0,0,0)

    -- print current layer title

    if layer < 0 then
        tstring = "Sub layer " .. tostring(math.abs(layer))
    elseif layer > 0 then
        tstring = "Super layer " .. tostring(layer)
    else
        tstring = ""
    end

    -- print current drawing mode

    if drawingMode ==  1 then
        dstring = "Line tool selected"
    elseif drawingMode == 2 then
        dstring = "Curve tool selected"
    end

    -- print last error message

    love.graphics.setFont(fontTiny)
    love.graphics.setColor(1,0,0)
    love.graphics.print(errorConsole, 25, 560)
    love.graphics.setColor(0,0,0)

    -- clear lineCanvas
    love.graphics.setCanvas(lineCanvas)
    love.graphics.clear()
    love.graphics.setCanvas()

    if viewingMode == 1 then
        
        love.graphics.setFont(font)
        love.graphics.printf(tstring, 0, 10, 800, "center")
        love.graphics.setFont(fontTiny)
        love.graphics.print(dstring, 10, 25)

        love.graphics.setColor(0,0,0,0.1)
        love.graphics.draw(grid, 46, 46)
        love.graphics.setColor(0,0,0,1)

        -- draw canonical points and connect appropriately
        i = 1
        while i < #points do
            
            if points[i].kind == "line" then

                love.graphics.setColor(1,0,0)
                love.graphics.rectangle("fill",points[i].x, points[i].y, 4, 4)
                i = i + 1
                love.graphics.rectangle("fill",points[i].x, points[i].y, 4, 4)
                love.graphics.setColor(0,0,0)

                love.graphics.setCanvas(lineCanvas)
                love.graphics.line(points[i].x + 2, points[i].y + 2, points[i-1].x + 2, points[i-1].y + 2)
                love.graphics.setCanvas()

            elseif points[i].kind == "bez" then

                love.graphics.setColor(0,0,1)
                love.graphics.rectangle("fill",points[i].x, points[i].y, 4, 4)
                i = i + 1
                love.graphics.rectangle("fill",points[i].x, points[i].y, 4, 4)
                i = i + 1
                love.graphics.rectangle("fill",points[i].x, points[i].y, 4, 4)
                i = i + 1
                love.graphics.rectangle("fill",points[i].x, points[i].y, 4, 4)
                love.graphics.setColor(0,0,0)

                curve = love.math.newBezierCurve(points[i - 3].x + 2, points[i - 3].y + 2, points[i - 2].x + 2, points[i - 2].y + 2, points[i - 1].x + 2, points[i - 1].y + 2, points[i].x + 2, points[i].y + 2)
                love.graphics.setCanvas(lineCanvas)
                love.graphics.line(curve:render())
                love.graphics.setCanvas()
                i = i + 1

            end

        end

        -- draw pending points
        if lastInsert == "line" then
            love.graphics.setColor(1,0,0)
            for _,p in ipairs(lineQueue) do
                love.graphics.rectangle("fill",p.x, p.y, 4, 4)
            end
            love.graphics.setColor(0,0,0)
        elseif lastInsert == "bez" then
            love.graphics.setColor(0,0,1)
            for _,p in ipairs(bezQueue) do
                love.graphics.rectangle("fill",p.x, p.y, 4, 4)
            end
            love.graphics.setColor(0,0,0)
        end

        love.graphics.draw(lineCanvas,0,0)

    end

    if viewingMode == 2 then
        love.graphics.printf("Connect below " .. tstring, 0, 10, 800, "center")

        pointsTransUpper = {}
        pointsTransLower = {}

        const = math.sqrt(2) / 2
        for __,point in ipairs(points) do
            x_temp = (0.75) * point[1] - 400
            y_temp = point[2] - 400
            x = (const * x_temp) + (const * -y_temp) + 400
            y = (((const * x_temp) + (const * y_temp) + 400) * (100/424))
            table.insert(pointsTransUpper, {x, y, 0, 0, 0})
        end

        lower = getLayerPoints(layer - 1)
        if lower == nil then
            lower = {}
        end

        for __,point in ipairs(lower) do
            x_temp = (0.75) * point[1] - 400
            y_temp = point[2] - 400
            x = (const * x_temp) + (const * -y_temp) + 400
            y = (((const * x_temp) + (const * y_temp) + 400) * (100/424))
            table.insert(pointsTransLower, {x, y, 0, 0, 0})
        end

        -- draw rhombi
        love.graphics.setColor(1,1,1)
        love.graphics.draw(rhombus,0,100)
        love.graphics.draw(rhombus,0,350)
        love.graphics.setColor(0,0,0)
        
        for i,point in ipairs(pointsTransLower) do
            
            love.graphics.rectangle("fill",point[1] - 5, point[2] + 400 - 5, 10, 10)

            if (i - 1) > 0 then
                love.graphics.line(point[1], point[2] + 400, pointsTransLower[i - 1][1], pointsTransLower[i - 1][2] + 400)
            end
            
        end

        for i,point in ipairs(pointsTransUpper) do
            
            love.graphics.rectangle("fill",point[1] - 5, point[2] + 150 - 5, 10, 10)

            if (i - 1) > 0 then
                love.graphics.line(point[1], point[2] + 150, pointsTransUpper[i - 1][1], pointsTransUpper[i - 1][2] + 150)
            end
            
        end
    end

    love.graphics.setColor(1,1,1)

end

function checkMouse()
    if (love.mouse.isDown(1)) then
        if mouse.justDown == false and mouse.pressed == false then
            mouse.justDown = true
            mouse.pressed = true
        else
            mouse.justDown = false
        end
    else
        mouse.justDown = false
        mouse.pressed = false
    end
end


