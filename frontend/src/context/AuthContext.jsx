import {createContext,useContext,useState} from 'react'
import api from '../lib/api'
const AuthContext=createContext(null)
export function AuthProvider({children}){const [user,setUser]=useState(()=>JSON.parse(localStorage.getItem('clinic_user')||'null'))
 const login=async(data)=>{const r=await api.post('/auth/login',data);localStorage.setItem('clinic_token',r.data.access_token);localStorage.setItem('clinic_user',JSON.stringify(r.data.user));setUser(r.data.user)}
 const register=async(data)=>{const r=await api.post('/auth/register',data);localStorage.setItem('clinic_token',r.data.access_token);localStorage.setItem('clinic_user',JSON.stringify(r.data.user));setUser(r.data.user)}
 const logout=()=>{localStorage.clear();setUser(null);window.location.href='/login'}
 return <AuthContext.Provider value={{user,login,register,logout}}>{children}</AuthContext.Provider>}
export const useAuth=()=>useContext(AuthContext)
