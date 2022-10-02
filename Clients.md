QMgr.dll in %windir%\System32 is the Microsoft client.
`get-item "C:\Windows\System32\qmgr.dll" | Select-Object -ExpandProperty VersionInfo`

Microsoft Versions
------------------
OS|BITS version|QMgr.dll file version|Symbolic class identifier
Server 2012 / Windows 8|BITS 5.0|7.7.xxxx.xxxx|CLSID_BackgroundCopyManager5_0
Server 2008 R2 / Windows 7|BITS 4.0|7.5.xxxx.xxxx|CLSID_BackgroundCopyManager4_0
Server 2008 / Vista|BITS 3.0|7.0.xxxx.xxxx|CLSID_BackgroundCopyManager3_0
Service Packs ?|BITS 2.5|6.7.xxxx.xxxx|CLSID_BackgroundCopyManager2_5
Server 2003sp1 / XPsp2|BITS 2.0|6.6.xxxx.xxxx|CLSID_BackgroundCopyManager2_0
Server 2003|BITS 1.5|6.5.xxxx.xxxx|CLSID_BackgroundCopyManager1_5
XPsp1|BITS 1.2|6.2.xxxx.xxxx|CLSID_BackgroundCopyManager
XP|BITS 1.0|6.0.xxxx.xxxx|CLSID_BackgroundCopyManager
Windows 10.0.19044 Build 19044||7.8.19041.1|


Notable BITS events
-------------------
 * Version 1.5 added support for uploads (only 1 per job).
 * Version 2.5 added support for certificate-based client authentication and IPv6.
 * Version 3.0 added Internet Gateway Device counters for bandwidth monitoring and PeerCache (for domain members).
 * Version 4.0 replaced PeerCache with BranchCache.
 * Version 5.0 IInterface improvements

 User Agents Seen in the Wild
 ----------------------------
 Windows reports the Qmgr.dll file version in the User-Agent field.
  * Windows 7 | Microsoft BITS/7.5
  * Windows 8.1 (v6.3) | User-Agent: Microsoft BITS/7.7
