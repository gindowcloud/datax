
export interface User {
  id?: string,
  name?: string,
}

export interface Connection {
  id?: string
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
  id?: string
  reader_id?: string
  writer_id?: string
  name?: string
  table?: string
  query?: string
  timer?: string
  executed_at?: string
}