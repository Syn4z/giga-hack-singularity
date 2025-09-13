export const getLocalStorageItem = (key: string): string | null => {
  return JSON.parse(localStorage.getItem(key) || 'null');
};

export const setLocalStorageItem = (key: string, data: string | null) => {
  localStorage.setItem(key, JSON.stringify(data));
};