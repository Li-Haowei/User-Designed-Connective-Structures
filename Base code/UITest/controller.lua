local controller = {}
controller.keys = {}
controller.ikeys = {}

local ButtonStateInstanceProps = {
}

local ButtonStateMT = {
    __index = ButtonStateInstanceProps
}

function controller.newButton(o, name)
    o = o or {}
    setmetatable(o, ButtonStateMT)
    o.JustPressed = false
    o.Down = false
    o.Released = false
    o.Up = true
    o.name = name
    return o
end

function controller.initButtons()
    controller.keys.down = controller.newButton(nil, "down")
    table.insert(controller.ikeys, controller.keys.down)
    controller.keys.up = controller.newButton(nil, "up")
    table.insert(controller.ikeys, controller.keys.up)
    controller.keys.right = controller.newButton(nil, "right")
    table.insert(controller.ikeys, controller.keys.right)
    controller.keys.left = controller.newButton(nil, "left")
    table.insert(controller.ikeys, controller.keys.left)
    controller.keys.space = controller.newButton(nil, "space")
    table.insert(controller.ikeys, controller.keys.space)
    controller.keys.a = controller.newButton(nil, "a")
    table.insert(controller.ikeys, controller.keys.a)
    controller.keys.z = controller.newButton(nil, "z")
    table.insert(controller.ikeys, controller.keys.z)
end

function controller.updateKeys()
    for _,key in ipairs(controller.ikeys) do
        if love.keyboard.isDown(key.name) then
            if not key.Down then
                key.Down = true
                key.JustPressed = true
                key.Released = false
                key.Up = false
            else
                key.Down = true
                key.JustPressed = false
                key.Released = false
                key.Up = false
            end
        else
            if not key.Up then
                key.Down = false
                key.JustPressed = false
                key.Released = true
                key.Up = true
            else
                key.Down = false
                key.JustPressed = false
                key.Released = false
                key.Up = true
            end
        end
    end
end

return controller