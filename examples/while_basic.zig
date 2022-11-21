const std = @import("std");

pub fn main() void {
    var x = 1;
    while (x < 10) : (x += 1) {
        std.debug.print("x = {}", .{});
    }
}

