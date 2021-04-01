module soc_top_tb();

logic clk;

initial begin
	clk = 1'b1;
end

always begin
	#1 clk = ~clk;
end

wire isp_uart_tx, vga_hsync, vga_vsync;
wire [ 2:0] vga_pixel;

soc_top soc_inst(
    .clk              ( clk          ),
    .isp_uart_rx      ( 1'b1         ),
    .isp_uart_tx      ( isp_uart_tx  ),
    .vga_hsync        ( vga_hsync    ),
    .vga_vsync        ( vga_vsync    ),
    .vga_red          ( vga_pixel[2] ),
    .vga_green        ( vga_pixel[1] ),
    .vga_blue         ( vga_pixel[0] )
);

initial begin
	#1000 $stop;
end

endmodule : soc_top_tb
