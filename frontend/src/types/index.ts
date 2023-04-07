
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
  table?: string
  query?: string
  timer?: string
  reader?: Connection
  writer?: Connection
  jobs?: Job[]
  executed_at?: string
}

export interface Job {
  id?: number
  state?: number
}