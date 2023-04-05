/**
 * 线拷贝对象
 * @param data 
 * @returns 
 */
export const $copy = (data: Object) => {
  return JSON.parse(JSON.stringify(data))
}