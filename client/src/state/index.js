// state/index.js
import { createSlice, configureStore } from '@reduxjs/toolkit'

const querySlice = createSlice({
  name: 'query',
  initialState: '',
  reducers: {
    setQuery: (state, action) => action.payload
  }
})

export const { setQuery } = querySlice.actions

const store = configureStore({
  reducer: {
    query: querySlice.reducer
  }
})

export default store
