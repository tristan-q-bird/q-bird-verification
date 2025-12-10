library ieee;
use ieee.std_logic_1164.all;

entity pipe is
    generic (
        DATA_WIDTH : positive;
        PIPE_DEPTH : natural
    );
    port ( 
        clk_i   : in std_logic;
        rst_i   : in std_logic;

        data_i  : in std_logic_vector(DATA_WIDTH - 1 downto 0);
        data_o  : out std_logic_vector(DATA_WIDTH - 1 downto 0)
    );
end;

architecture rtl of pipe is
    subtype data_t is std_logic_vector(DATA_WIDTH - 1 downto 0);
    type pipe_t is array (PIPE_DEPTH - 1 downto 0) of data_t;
begin
    
    g_pipe : if PIPE_DEPTH = 0 generate
        data_o <= data_i;
    elsif PIPE_DEPTH = 1 generate
        p_pipe : process (clk_i) begin
            if rising_edge(clk_i) then
                if rst_i then
                    data_o <= ( others => '0' );
                else
                    data_o <= data_i;
                end if;
            end if;
        end process;
    else generate
        signal data_pipe : pipe_t;
    begin
        p_pipe : process (clk_i) begin
            if rising_edge(clk_i) then
                if rst_i then
                    data_pipe <= ( others => ( others => '0' ) );
                else
                    data_pipe(data_pipe'right) <= data_i;
                    data_pipe(data_pipe'left downto 1) <= data_pipe(data_pipe'left - 1 downto 0);
                end if;
            end if;
        end process;

        data_o <= data_pipe(data_pipe'left);
    end generate;

end;