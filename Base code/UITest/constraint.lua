local constraint = {}

function constraint.isClose(val1, val2)
    eps = 1e-6
    return math.abs(val1 - val2) < eps
end

function constraint.checkG1(p1, p2, p3, p4)
    if p3 == nil and p4 == nil then
        return true
    end

    if (p4.x - p3.x == 0) or (p2.x - p1.x == 0) then
        if (p4.x - p3.x == 0) and (p2.x - p1.x == 0) then
            return true
        else
            return false
        end
    end

    prevSlope = (p4.y - p3.y)/(p4.x - p3.x)
    newSlope = (p2.y - p1.y)/(p2.x - p1.x)

    return constraint.isClose(prevSlope, newSlope)

end

return constraint