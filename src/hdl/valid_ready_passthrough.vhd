library ieee;
use ieee.std_logic_1164.all;

entity valid_ready_passthrough is
    generic (
        DATA_WIDTH : positive
    );
    port ( 
        clk_i   : in std_logic; -- Not used in this module but the tb wants it

        data_i  : in std_logic_vector(DATA_WIDTH - 1 downto 0);
        valid_i : in std_logic;
        ready_o : out std_logic;

        data_o  : out std_logic_vector(DATA_WIDTH - 1 downto 0);
        valid_o : out std_logic;
        ready_i : in std_logic
    );
end;

architecture rtl of valid_ready_passthrough is
begin
    data_o  <= data_i;
    valid_o <= valid_i;
    ready_o <= ready_i;
end;