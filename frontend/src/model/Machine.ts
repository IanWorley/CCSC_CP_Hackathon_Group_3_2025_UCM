export interface Machine {
  id: number;
  state: string;
  state_init_time: number;
  type: string;
  will_reserve: boolean;
}
