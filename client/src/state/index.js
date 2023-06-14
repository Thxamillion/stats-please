import { createSlice, configureStore } from '@reduxjs/toolkit'

const querySlice = createSlice({
  name: 'query',
  initialState: { query: '', loading: false },
  reducers: {
    setQuery: (state, action) => {
      state.query = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    }
  }
})

export const { setQuery, setLoading } = querySlice.actions

const store = configureStore({
  reducer: {
    query: querySlice.reducer
  }
})

export default store
