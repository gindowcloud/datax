
export interface User {
  id?: number,
  username?: string,
  password?: string,
  name?: string,
  state?: number
}

export interface Connection {
  id?: number
  direct?: string
  driver?: string
  name?: string
  host?: string
  port?: string
  username?: string
  password?: string
  database?: string
}

export interface Task {
  id?: number
  reader_id?: number
  writer_id?: number
  name?: string
  query?: string
  date?: string
  table?: string
  column?: string
  timer?: string
  reader?: Connection
  writer?: Connection
  jobs?: Job[]
  executed_at?: string
  incremental?: boolean
}

export interface Job {
  id?: number
  state?: number
}

export interface Schedule {
  id?: number
  task_id?: number
  name?: string
  type?: string
  date?: string
  cron?: string
  interval?: number
  period?: string
}
