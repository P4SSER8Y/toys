#SingleInstance force

SetWorkingDir, %A_ScriptDir%
Menu,Tray,Tip,INTERESTING
Menu,Tray,NoStandard
Menu,Tray,Add,restart,fnRestart
Menu,Tray,Default,restart
Menu,Tray,Add,pause,fnPause
Menu,Tray,Add,biu~,fnExit

traytip,=?????=,Hallo Welt,10,0x1

EnableDeutsch := false
EnableLisp := false
EnableExchangeCtrlAlt := false

return 

^CAPSLOCK::
    if GetKeyState("Capslock","T")
        SetCapslockState, Off
    else
        SetCapslockState, On
return


;=== Modified RAlt as Fn ===
*>!w::Send {Up}
*>!a::Send {Left}
*>!s::Send {Down}
*>!d::Send {Right}


;=== Modified App to Fn, acting like Poker ===
AppsKey & a:: Send {Left}
AppsKey & s:: Send {Down}
AppsKey & w:: Send {Up}
AppsKey & d:: Send {Right}

AppsKey & n:: Send {Volume_Down}
AppsKey & m:: Send {Volume_Up}
AppsKey & ,:: Send {Volume_Mute}

AppsKey & 1:: Send {F1}
AppsKey & 2:: Send {F2}
AppsKey & 3:: Send {F3}
AppsKey & 4:: Send {F4}
AppsKey & 5:: Send {F5}
AppsKey & 6:: Send {F6}
AppsKey & 7:: Send {F7}
AppsKey & 8:: Send {F8}
AppsKey & 9:: Send {F9}
AppsKey & 0:: Send {F10}

AppsKey & Backspace:: Send {Delete}
AppsKey & .:: Send {End}
AppsKey & SC027:: Send {Home}
AppsKey & ':: Send {PgUp}
AppsKey & /:: Send {PgDn}
AppsKey & p:: Send {PrintScreen}


;=== MISC ===
CAPSLOCK::ESC
#F1::^#Left
!1::Send ^#{Left}
#F2::^#Right
!2::Send ^#{Right}
!4::Send !{F4}
#NUMPAD3::#L

;=== Mouse ===
XButton1::PgDn
XButton2::PgUp


;=== File Open/Save Dialog === 
#IfWinActive ahk_class #32770
XButton1::!Up

;=== File Manager ===
#IfWinActive ahk_class CabinetWClass
!XButton1::!Up
^XButton2::^+n
XButton1::PgDn
XButton2::PgUp

;=== Win+R ===
#If WinActive("????") and WinActive("AHK_CLASS #32770") and WinActive("AHK_EXE explorer.exe")
TAB::Enter


fnRestart:
    Reload
return

fnPause:
    Suspend ,Toggle
return

fnExit:
    ExitApp
return

fnNone:
return
