
export interface User {
  id?: string,
  name?: string,
}

export interface Connection {
  id?: string
  name?: string
  driver?: string
  host?: string
  port?: string
  username?: string
  password?: string
  database?: string
}
