const std = @import("std");

pub fn main() !void {
    const stdin = std.io.getStdIn().reader();
    var buf: [100]u8 = undefined;
    const line = try stdin.readUntilDelimiter(&buf, '\n');
    _ = line;
}
