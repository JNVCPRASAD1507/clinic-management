import {NavLink,Outlet,useNavigate} from "react-router-dom";
import {CalendarDays,ChevronRight,ClipboardList,FileText,LayoutDashboard,LogOut,Menu,Stethoscope,Users,UserRound,BarChart3,X} from "lucide-react";
import {useAuth} from "../context/AuthContext";
import {useState} from "react";
const links=[
 {to:"/",label:"Dashboard",icon:LayoutDashboard,roles:["Admin","Doctor","Receptionist"]},
 {to:"/appointments",label:"Appointments",icon:CalendarDays,roles:["Admin","Doctor","Receptionist"]},
 {to:"/patients",label:"Patients",icon:Users,roles:["Admin","Doctor","Receptionist"]},
 {to:"/doctors",label:"Doctors",icon:Stethoscope,roles:["Admin","Doctor","Receptionist"]},
 {to:"/prescriptions",label:"Prescriptions",icon:ClipboardList,roles:["Admin","Doctor"]},
 {to:"/records",label:"Medical Records",icon:FileText,roles:["Admin","Doctor","Receptionist"]},
 {to:"/reports",label:"Reports",icon:BarChart3,roles:["Admin"]}
];
export default function Layout(){
 const {user,logout}=useAuth(); const [open,setOpen]=useState(false); const nav=useNavigate();
 const visible=links.filter(x=>x.roles.includes(user?.role));
 const signout=()=>{logout();nav("/login");};
 return <div className="min-h-screen bg-slate-50">
  <aside className={`fixed inset-y-0 left-0 z-40 w-64 border-r border-slate-200 bg-white transition-transform lg:translate-x-0 ${open?"translate-x-0":"-translate-x-full"}`}>
   <div className="flex h-16 items-center justify-between border-b px-5"><div className="flex items-center gap-2 font-bold text-slate-900"><span className="grid h-9 w-9 place-items-center rounded-xl bg-brand-700 text-white"><Stethoscope size={19}/></span>CareFlow</div><button className="lg:hidden" onClick={()=>setOpen(false)}><X/></button></div>
   <div className="px-3 py-5"><p className="px-3 pb-2 text-[10px] font-bold uppercase tracking-[.18em] text-slate-400">Workspace</p>{visible.map(({to,label,icon:Icon})=><NavLink key={to} to={to} onClick={()=>setOpen(false)} className={({isActive})=>`mb-1 flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium ${isActive?"bg-brand-50 text-brand-700":"text-slate-600 hover:bg-slate-50"}`}><Icon size={18}/>{label}</NavLink>)}</div>
   <div className="absolute bottom-0 w-full border-t p-4"><div className="mb-3 rounded-xl bg-slate-50 p-3"><p className="truncate text-sm font-semibold">{user?.full_name}</p><p className="text-xs text-slate-500">{user?.role}</p></div><button onClick={signout} className="flex w-full items-center gap-2 rounded-xl px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50"><LogOut size={17}/>Sign out</button></div>
  </aside>
  <div className="lg:pl-64"><header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white/90 px-4 backdrop-blur lg:px-8"><button className="lg:hidden" onClick={()=>setOpen(true)}><Menu/></button><div className="ml-auto flex items-center gap-3"><div className="hidden text-right sm:block"><p className="text-sm font-semibold">{user?.full_name}</p><p className="text-xs text-slate-500">{user?.email}</p></div><div className="grid h-9 w-9 place-items-center rounded-full bg-brand-100 text-sm font-bold text-brand-700">{user?.full_name?.slice(0,1)?.toUpperCase()}</div></div></header><main className="p-4 lg:p-8"><Outlet/></main></div>
 </div>
}
