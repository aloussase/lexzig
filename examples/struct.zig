const Circle = struct {
    x: i32,
    y: i32,

    pub fn new(x: i32, y: i32) Circle {
        return Circle{ .x = x, .y = y };
    }
};
