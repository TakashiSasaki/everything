# Everything SDK Reference

<!-- TOC START -->
## Table of Contents
- [Everything_CleanUp](#everything_cleanup)
- [Everything_DeleteRunHistory](#everything_deleterunhistory)
- [Everything_Exit](#everything_exit)
- [Everything_GetBuildNumber](#everything_getbuildnumber)
- [Everything_GetLastError](#everything_getlasterror)
- [Everything_GetMajorVersion](#everything_getmajorversion)
- [Everything_GetMatchCase](#everything_getmatchcase)
- [Everything_GetMatchPath](#everything_getmatchpath)
- [Everything_GetMatchWholeWord](#everything_getmatchwholeword)
- [Everything_GetMax](#everything_getmax)
- [Everything_GetMinorVersion](#everything_getminorversion)
- [Everything_GetNumFileResults](#everything_getnumfileresults)
- [Everything_GetNumFolderResults](#everything_getnumfolderresults)
- [Everything_GetNumResults](#everything_getnumresults)
- [Everything_GetOffset](#everything_getoffset)
- [Everything_GetRegex](#everything_getregex)
- [Everything_GetReplyID](#everything_getreplyid)
- [Everything_GetReplyWindow](#everything_getreplywindow)
- [Everything_GetRequestFlags](#everything_getrequestflags)
- [Everything_GetResultAttributes](#everything_getresultattributes)
- [Everything_GetResultDateAccessed](#everything_getresultdateaccessed)
- [Everything_GetResultDateCreated](#everything_getresultdatecreated)
- [Everything_GetResultDateModified](#everything_getresultdatemodified)
- [Everything_GetResultDateRecentlyChanged](#everything_getresultdaterecentlychanged)
- [Everything_GetResultDateRun](#everything_getresultdaterun)
- [Everything_GetResultExtension](#everything_getresultextension)
- [Everything_GetResultFileListFileName](#everything_getresultfilelistfilename)
- [Everything_GetResultFileName](#everything_getresultfilename)
- [Everything_GetResultFullPathName](#everything_getresultfullpathname)
- [Everything_GetResultHighlightedFileName](#everything_getresulthighlightedfilename)
- [Everything_GetResultHighlightedFullPathAndFileName](#everything_getresulthighlightedfullpathandfilename)
- [Everything_GetResultHighlightedPath](#everything_getresulthighlightedpath)
- [Everything_GetResultListRequestFlags](#everything_getresultlistrequestflags)
- [Everything_GetResultListSort](#everything_getresultlistsort)
- [Everything_GetResultPath](#everything_getresultpath)
- [Everything_GetResultRunCount](#everything_getresultruncount)
- [Everything_GetResultSize](#everything_getresultsize)
- [Everything_GetRevision](#everything_getrevision)
- [Everything_GetRunCountFromFileName](#everything_getruncountfromfilename)
- [Everything_GetSearch](#everything_getsearch)
- [Everything_GetSort](#everything_getsort)
- [Everything_GetTargetMachine](#everything_gettargetmachine)
- [Everything_GetTotFileResults](#everything_gettotfileresults)
- [Everything_GetTotFolderResults](#everything_gettotfolderresults)
- [Everything_GetTotResults](#everything_gettotresults)
- [Everything_IncRunCountFromFileName](#everything_incruncountfromfilename)
- [Everything_IsAdmin](#everything_isadmin)
- [Everything_IsAppData](#everything_isappdata)
- [Everything_IsDBLoaded](#everything_isdbloaded)
- [Everything_IsFastSort](#everything_isfastsort)
- [Everything_IsFileInfoIndexed](#everything_isfileinfoindexed)
- [Everything_IsFileResult](#everything_isfileresult)
- [Everything_IsFolderResult](#everything_isfolderresult)
- [Everything_IsQueryReply](#everything_isqueryreply)
- [Everything_IsVolumeResult](#everything_isvolumeresult)
- [Everything_Query](#everything_query)
- [Everything_RebuildDB](#everything_rebuilddb)
- [Everything_Reset](#everything_reset)
- [Everything_SaveDB](#everything_savedb)
- [Everything_SaveRunHistory](#everything_saverunhistory)
- [Everything_SetMatchCase](#everything_setmatchcase)
- [Everything_SetMatchPath](#everything_setmatchpath)
- [Everything_SetMatchWholeWord](#everything_setmatchwholeword)
- [Everything_SetMax](#everything_setmax)
- [Everything_SetOffset](#everything_setoffset)
- [Everything_SetRegex](#everything_setregex)
- [Everything_SetReplyID](#everything_setreplyid)
- [Everything_SetReplyWindow](#everything_setreplywindow)
- [Everything_SetRequestFlags](#everything_setrequestflags)
- [Everything_SetRunCountFromFileName](#everything_setruncountfromfilename)
- [Everything_SetSearch](#everything_setsearch)
- [Everything_SetSort](#everything_setsort)
- [Everything_SortResultsByPath](#everything_sortresultsbypath)
- [Everything_UpdateAllFolderIndexes](#everything_updateallfolderindexes)
<!-- TOC END -->


This document aggregates function reference pages from the Everything wiki.

## everything cleanup

Source: https://www.voidtools.com/support/everything/sdk/everything_cleanup

## Everything_CleanUp
The Everything_CleanUp function frees any allocated memory by the library.

### Syntax
```
void Everything_CleanUp(void);
```

### Parameters
This function has no parameters.

### Return Value
This function has no return value.

### Remarks
You should call Everything_CleanUp to free any memory allocated by the Everything SDK.

Everything_CleanUp should be the last call to the Everything SDK.

Call Everything_Reset to free any allocated memory for the current search and results.

Everything_Reset will also reset the search and result state to their defaults.

Calling Everything_SetSearch frees the old search and allocates the new search string.

Calling Everything_Query frees the old result list and allocates the new result list.

### Example
```
Everything_CleanUp();
```

### See Also
- Everything_SetSearch
- Everything_Reset
- Everything_Query

## everything deleterunhistory

Source: https://www.voidtools.com/support/everything/sdk/everything_deleterunhistory

## Everything_DeleteRunHistory
The Everything_DeleteRunHistory function deletes all run history.

### Syntax
```
BOOL Everything_DeleteRunHistory(void);
```

### Parameters
No parameters.

### Return Value
The function returns non-zero if run history is cleared.

The function returns 0 if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Calling this function will clear all run history from memory and disk.

### Example
```
// clear run history
Everything_DeleteRunHistory();
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_GetRunCountFromFileName
- Everything_SetRunCountFromFileName
- Everything_IncRunCountFromFileName

## everything exit

Source: https://www.voidtools.com/support/everything/sdk/everything_exit

## Everything_Exit
The Everything_Exit function requests Everything to exit.

### Syntax
```
BOOL Everything_Exit(void);
```

### Parameters
No parameters.

### Return Value
The function returns non-zero if the exit request was successful.

The function returns 0 if the request failed. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Request Everything to save settings and data to disk and exit.

### Example
```
// request Everything to exit.
Everything_Exit();
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also

## everything getbuildnumber

Source: https://www.voidtools.com/support/everything/sdk/everything_getbuildnumber

## Everything_GetBuildNumber
The Everything_GetBuildNumber function retrieves the build number of Everything.

### Syntax
```
DWORD Everything_GetBuildNumber(void);
```

### Parameters
No parameters.

### Return Value
The function returns the build number.

The function returns 0 if build information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Everything uses the following version format:

major.minor.revision.build

The build part is incremental and unique for all Everything versions.

### Example
```
DWORD buildNumber;
// get the build number 
buildNumber = Everything_GetBuildNumber();
if (buildNumber >= 686)
{
	// do something with build 686 or later.
}
```

### Function Information
Requires Everything 1.0.0.0 or later.

### See Also
- Everything_GetMajorVersion
- Everything_GetMinorVersion
- Everything_GetRevision
- Everything_GetTargetMachine

## everything getlasterror

Source: https://www.voidtools.com/support/everything/sdk/everything_getlasterror

## Everything_GetLastError
The Everything_GetLastError function retrieves the last-error code value.

### Syntax
```
DWORD Everything_GetLastError(void);
```

### Parameters
This function has no parameters.

### Return Value
Error code
Value
Meaning
EVERYTHING_OK
0
The operation completed successfully.
EVERYTHING_ERROR_MEMORY
1
Failed to allocate memory for the search query.
EVERYTHING_ERROR_IPC
2
IPC is not available.
EVERYTHING_ERROR_REGISTERCLASSEX
3
Failed to register the search query window class.
EVERYTHING_ERROR_CREATEWINDOW
4
Failed to create the search query window.
EVERYTHING_ERROR_CREATETHREAD
5
Failed to create the search query thread. 
EVERYTHING_ERROR_INVALIDINDEX
6
Invalid index. The index must be greater or equal to 0 and less than the number of visible results.
EVERYTHING_ERROR_INVALIDCALL
7
Invalid call.
### Example
```
// execute the query
if (!Everything_Query(true))
{
	DWORD dwLastError = Everything_GetLastError();
	if (dwLastError == EVERYTHING_ERROR_IPC)
	{
		// IPC not available.
	}
}
```

## everything getmajorversion

Source: https://www.voidtools.com/support/everything/sdk/everything_getmajorversion

## Everything_GetMajorVersion
The Everything_GetMajorVersion function retrieves the major version number of Everything.

### Syntax
```
DWORD Everything_GetMajorVersion(void);
```

### Parameters
No parameters.

### Return Value
The function returns the major version number.

The function returns 0 if major version information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Everything uses the following version format:

major.minor.revision.build

The build part is incremental and unique for all Everything versions.

### Example
```
DWORD majorVersion;
DWORD minorVersion;
DWORD revision;
// get version information
majorVersion = Everything_GetMajorVersion();
minorVersion = Everything_GetMinorVersion();
revision = Everything_GetRevision();
if ((majorVersion > 1) || ((majorVersion == 1) && (minorVersion > 3)) || ((majorVersion == 1) && (minorVersion == 3) && (revision >= 4)))
{
	// do something with version 1.3.4 or later
}
```

### Function Information
Requires Everything 1.0.0.0 or later.

### See Also
- Everything_GetMinorVersion
- Everything_GetRevision
- Everything_GetBuildNumber
- Everything_GetTargetMachine

## everything getmatchcase

Source: https://www.voidtools.com/support/everything/sdk/everything_getmatchcase

## Everything_GetMatchCase
The Everything_GetMatchCase function returns the match case state.

### Syntax
```
BOOL Everything_GetMatchCase(void);
```

### Return Value
The return value is the match case state.

The function returns TRUE if match case is enabled.

The function returns FALSE if match case is disabled.

### Remarks
Get the internal state of the match case switch.

The default state is FALSE, or disabled.

### Example
```
BOOL bEnabled = Everything_GetMatchCase();
```

### See Also
- Everything_SetMatchCase
- Everything_Query

## everything getmatchpath

Source: https://www.voidtools.com/support/everything/sdk/everything_getmatchpath

## Everything_GetMatchPath
The Everything_GetMatchPath function returns the state of the match full path switch.

### Syntax
```
BOOL Everything_GetMatchPath(void);
```

### Return Value
The return value is the state of the match full path switch.

The function returns TRUE if match full path is enabled.

The function returns FALSE if match full path is disabled.

### Remarks
Get the internal state of the match full path switch.

The default state is FALSE, or disabled.

### Example
```
BOOL bEnabled = Everything_GetMatchPath();
```

### See Also
- Everything_SetMatchPath
- Everything_Query

## everything getmatchwholeword

Source: https://www.voidtools.com/support/everything/sdk/everything_getmatchwholeword

## Everything_GetMatchWholeWord
The Everything_GetMatchWholeWord function returns the match whole word state.

### Syntax
```
BOOL Everything_GetMatchWholeWord(void);
```

### Return Value
The return value is the match whole word state.

The function returns TRUE if match whole word is enabled.

The function returns FALSE if match whole word is disabled.

### Remarks
The default state is FALSE, or disabled.

### Example
```
BOOL bEnabled = Everything_GetMatchWholeWord();
```

### See Also
- Everything_SetMatchWholeWord
- Everything_Query

## everything getmax

Source: https://www.voidtools.com/support/everything/sdk/everything_getmax

## Everything_GetMax
The Everything_GetMax function returns the maximum number of results state.

### Syntax
```
BOOL Everything_GetMax(void);
```

### Return Value
The return value is the maximum number of results state.

The function returns 0xFFFFFFFF if all results should be returned.

### Remarks
The default state is 0xFFFFFFFF, or all results.

### Example
```
DWORD dwMaxResults = Everything_GetMax();
```

### See Also
- Everything_SetMax
- Everything_Query

## everything getminorversion

Source: https://www.voidtools.com/support/everything/sdk/everything_getminorversion

## Everything_GetMinorVersion
The Everything_GetMinorVersion function retrieves the minor version number of Everything.

### Syntax
```
DWORD Everything_GetMinorVersion(void);
```

### Parameters
No parameters.

### Return Value
The function returns the minor version number.

The function returns 0 if minor version information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Everything uses the following version format:

major.minor.revision.build

The build part is incremental and unique for all Everything versions.

### Example
```
DWORD majorVersion;
DWORD minorVersion;
DWORD revision;
// get version information
majorVersion = Everything_GetMajorVersion();
minorVersion = Everything_GetMinorVersion();
revision = Everything_GetRevision();
if ((majorVersion > 1) || ((majorVersion == 1) && (minorVersion > 3)) || ((majorVersion == 1) && (minorVersion == 3) && (revision >= 4)))
{
	// do something with version 1.3.4 or later
}
```

### Function Information
Requires Everything 1.0.0.0 or later.

### See Also
- Everything_GetMajorVersion
- Everything_GetRevision
- Everything_GetBuildNumber
- Everything_GetTargetMachine

## everything getnumfileresults

Source: https://www.voidtools.com/support/everything/sdk/everything_getnumfileresults

## Everything_GetNumFileResults
The Everything_GetNumFileResults function returns the number of visible file results.

### Syntax
```
DWORD Everything_GetNumFileResults(void);
```

### Parameters
This functions has no parameters.

### Return Value
Returns the number of visible file results.

If the function fails the return value is 0. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetNumFileResults.
### Remarks
You must call Everything_Query before calling Everything_GetNumFileResults.

Use Everything_GetTotFileResults to retrieve the total number of file results.

If the result offset state is 0, and the max result is 0xFFFFFFFF, Everything_GetNumFileResults will return the total number of file results and all file results will be visible.

Everything_GetNumFileResults is not supported when using Everything_SetRequestFlags

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// get the number of visible file results.
DWORD dwNumFileResults = Everything_GetNumFileResults();
```

### See Also
- Everything_Query
- Everything_GetNumResults
- Everything_GetNumFolderResults
- Everything_GetTotResults
- Everything_GetTotFileResults
- Everything_GetTotFolderResults

## everything getnumfolderresults

Source: https://www.voidtools.com/support/everything/sdk/everything_getnumfolderresults

## Everything_GetNumFolderResults
The Everything_GetNumFolderResults function returns the number of visible folder results.

### Syntax
```
DWORD Everything_GetNumFolderResults(void);
```

### Parameters
This functions has no parameters.

### Return Value
Returns the number of visible folder results.

If the function fails the return value is 0. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetNumFolderResults.
### Remarks
You must call Everything_Query before calling Everything_GetNumFolderResults.

Use Everything_GetTotFolderResults to retrieve the total number of folder results.

If the result offset state is 0, and the max result is 0xFFFFFFFF, Everything_GetNumFolderResults will return the total number of folder results and all folder results will be visible.

Everything_GetNumFolderResults is not supported when using Everything_SetRequestFlags

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// get the number of visible folder results
DWORD dwNumFolderResults = Everything_GetNumFolderResults();
```

### See Also
- Everything_Query
- Everything_GetNumResults
- Everything_GetNumFileResults
- Everything_GetTotResults
- Everything_GetTotFileResults
- Everything_GetTotFolderResults

## everything getnumresults

Source: https://www.voidtools.com/support/everything/sdk/everything_getnumresults

## Everything_GetNumResults
The Everything_GetNumResults function returns the number of visible file and folder results.

### Syntax
```
DWORD Everything_GetNumResults(void);
```

### Parameters
This functions has no parameters.

### Return Value
Returns the number of visible file and folder results.

If the function fails the return value is 0. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetNumResults.
### Remarks
You must call Everything_Query before calling Everything_GetNumResults.

Use Everything_GetTotResults to retrieve the total number of file and folder results.

If the result offset state is 0, and the max result is 0xFFFFFFFF, Everything_GetNumResults will return the total number of file and folder results and all file and folder results will be visible.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// get the number of visible file and folder results.
DWORD dwNumResults = Everything_GetNumResults();
```

### See Also
- Everything_Query
- Everything_GetNumFileResults
- Everything_GetNumFolderResults
- Everything_GetTotResults
- Everything_GetTotFileResults
- Everything_GetTotFolderResults

## everything getoffset

Source: https://www.voidtools.com/support/everything/sdk/everything_getoffset

## Everything_GetOffset
The Everything_GetOffset function returns the first item offset of the available results.

### Syntax
```
DWORD Everything_GetOffset(void);
```

### Return Value
The return value is the first item offset.

### Remarks
The default offset is 0.

### Example
```
DWORD dwOffset = Everything_GetOffset();
```

### See Also
- Everything_SetOffset
- Everything_Query

## everything getregex

Source: https://www.voidtools.com/support/everything/sdk/everything_getregex

## Everything_GetRegex
The Everything_GetRegex function returns the regex state.

### Syntax
```
BOOL Everything_GetRegex(void);
```

### Return Value
The return value is the regex state.

The function returns TRUE if regex is enabled.

The function returns FALSE if regex is disabled.

### Remarks
The default state is FALSE.

### Example
```
BOOL bRegex = Everything_GetRegex();
```

### See Also
- Everything_SetRegex
- Everything_Query

## everything getreplyid

Source: https://www.voidtools.com/support/everything/sdk/everything_getreplyid

## Everything_GetReplyID
The Everything_GetReplyID function returns the current reply identifier for the IPC query reply.

### Syntax
```
DWORD Everything_GetReplyID(void);
```

### Return Value
The return value is the current reply identifier.

### Remarks
The default reply identifier is 0.

### Example
```
DWORD id = Everything_GetReplyID();
```

### See Also
- Everything_SetReplyWindow
- Everything_GetReplyWindow
- Everything_SetReplyID
- Everything_Query
- Everything_IsQueryReply

## everything getreplywindow

Source: https://www.voidtools.com/support/everything/sdk/everything_getreplywindow

## Everything_GetReplyWindow
The Everything_GetReplyWindow function returns the current reply window for the IPC query reply.

### Syntax
```
HWND Everything_GetReplyWindow(void);
```

### Return Value
The return value is the current reply window.

### Remarks
The default reply window is 0, or no reply window.

### Example
```
HWND hWnd = Everything_GetReplyWindow();
```

### See Also
- Everything_SetReplyWindow
- Everything_SetReplyID
- Everything_GetReplyID
- Everything_Query
- Everything_IsQueryReply

## everything getrequestflags

Source: https://www.voidtools.com/support/everything/sdk/everything_getrequestflags

## Everything_GetRequestFlags
The Everything_GetRequestFlags function returns the desired result data flags.

### Syntax
```
DWORD Everything_GetRequestFlags(void);
```

### Return Value
Returns zero or more of the following request flags:

```
EVERYTHING_REQUEST_FILE_NAME                            (0x00000001)
EVERYTHING_REQUEST_PATH                                 (0x00000002)
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME              (0x00000004)
EVERYTHING_REQUEST_EXTENSION                            (0x00000008)
EVERYTHING_REQUEST_SIZE                                 (0x00000010)
EVERYTHING_REQUEST_DATE_CREATED                         (0x00000020)
EVERYTHING_REQUEST_DATE_MODIFIED                        (0x00000040)
EVERYTHING_REQUEST_DATE_ACCESSED                        (0x00000080)
EVERYTHING_REQUEST_ATTRIBUTES                           (0x00000100)
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME                  (0x00000200)
EVERYTHING_REQUEST_RUN_COUNT                            (0x00000400)
EVERYTHING_REQUEST_DATE_RUN                             (0x00000800)
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED                (0x00001000)
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME                (0x00002000)
EVERYTHING_REQUEST_HIGHLIGHTED_PATH                     (0x00004000)
EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME  (0x00008000)
```

### Remarks
The default request flags are EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH (0x00000003)

### Example
```
DWORD dwRequestFlags = Everything_GetRequestFlags();
```

### See Also
- Everything_SetRequestFlags
- Everything_Query

## everything getresultattributes

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultattributes

## Everything_GetResultAttributes
The Everything_GetResultAttributes function retrieves the attributes of a visible result.

### Syntax
```
DWORD Everything_GetResultAttributes(
    DWORD dwIndex,
);
```

### Parameters
dwIndex

Zero based index of the visible result.

### Return Value
The function returns zero or more of FILE_ATTRIBUTE_* flags.

The function returns INVALID_FILE_ATTRIBUTES if attribute information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultAttributes.
EVERYTHING_ERROR_INVALIDREQUEST
Attribute information was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_ATTRIBUTES before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
dwIndex must be a valid visible result index. To determine if a result index is visible use the Everything_GetNumResults function.

### Example
```
DWORD attributes;
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the attributes of the first visible result.
attributes = Everything_GetResultAttributes(0);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultdateaccessed

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultdateaccessed

## Everything_GetResultDateAccessed
The Everything_GetResultDateAccessed function retrieves the accessed date of a visible result.

### Syntax
```
BOOL Everything_GetResultDateAccessed(
    DWORD dwIndex,
    FILETIME *lpDateAccessed
);
```

### Parameters
dwIndex

Zero based index of the visible result.

lpDateAccessed

Pointer to a FILETIME to hold the accessed date of the result.

### Return Value
The function returns non-zero if successful.

The function returns 0 if the accessed date information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultDateAccessed.
EVERYTHING_ERROR_INVALIDREQUEST
Accessed date was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_DATE_ACCESSED before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
dwIndex must be a valid visible result index. To determine if a result index is visible use the Everything_GetNumResults function.

### Example
```
FILETIME dateAccessed;
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the accessed date of the first visible result.
Everything_GetResultDateAccessed(0,&dateAccessed);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultdatecreated

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultdatecreated

## Everything_GetResultDateCreated
The Everything_GetResultDateCreated function retrieves the created date of a visible result.

### Syntax
```
BOOL Everything_GetResultDateCreated(
    DWORD dwIndex,
    FILETIME *lpDateCreated
);
```

### Parameters
dwIndex

Zero based index of the visible result.

lpDateCreated

Pointer to a FILETIME to hold the created date of the result.

### Return Value
The function returns non-zero if successful.

The function returns 0 if the date created information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultDateCreated.
EVERYTHING_ERROR_INVALIDREQUEST
Date created was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_DATE_CREATED before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
dwIndex must be a valid visible result index. To determine if a result index is visible use the Everything_GetNumResults function.

### Example
```
FILETIME dateCreated;
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the created date of the first visible result.
Everything_GetResultDateCreated(0,&dateCreated);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultdatemodified

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultdatemodified

## Everything_GetResultDateModified
The Everything_GetResultDateModified function retrieves the modified date of a visible result.

### Syntax
```
BOOL Everything_GetResultDateModified(
    DWORD dwIndex,
    FILETIME *lpDateModified
);
```

### Parameters
dwIndex

Zero based index of the visible result.

lpDateModified

Pointer to a FILETIME to hold the modified date of the result.

### Return Value
The function returns non-zero if successful.

The function returns 0 if the modified date information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultDateModified.
EVERYTHING_ERROR_INVALIDREQUEST
Modified date was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_DATE_MODIFIED before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
dwIndex must be a valid visible result index. To determine if a result index is visible use the Everything_GetNumResults function.

### Example
```
FILETIME dateModified;
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the modified date of the first visible result.
Everything_GetResultDateModified(0,&dateModified);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultdaterecentlychanged

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultdaterecentlychanged

## Everything_GetResultDateRecentlyChanged
The Everything_GetResultDateRecentlyChanged function retrieves the recently changed date of a visible result.

### Syntax
```
BOOL Everything_GetResultDateRecentlyChanged(
    DWORD dwIndex,
    FILETIME *lpDateRecentlyChanged
);
```

### Parameters
dwIndex

Zero based index of the visible result.

lpDateRecentlyChanged

Pointer to a FILETIME to hold the recently changed date of the result.

### Return Value
The function returns non-zero if successful.

The function returns 0 if the recently changed date information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultDateRecentlyChanged.
EVERYTHING_ERROR_INVALIDREQUEST
Recently changed date was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
dwIndex must be a valid visible result index. To determine if a result index is visible use the Everything_GetNumResults function.

The date recently changed is the date and time of when the result was changed in the Everything index, this could be from a file creation, rename, attribute or content change.

### Example
```
FILETIME dateRecentlyChanged;
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the recently changed date of the first visible result.
Everything_GetResultDateRecentlyChanged(0,&dateRecentlyChanged);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultdaterun

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultdaterun

## Everything_GetResultDateRun
The Everything_GetResultDateRun function retrieves the run date of a visible result.

### Syntax
```
BOOL Everything_GetResultDateRun(
    DWORD dwIndex,
    FILETIME *lpDateRun
);
```

### Parameters
dwIndex

Zero based index of the visible result.

lpDateRun

Pointer to a FILETIME to hold the Run date of the result.

### Return Value
The function returns non-zero if successful.

The function returns 0 if the run date information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultDateRun.
EVERYTHING_ERROR_INVALIDREQUEST
Run date was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_DATE_RUN before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
dwIndex must be a valid visible result index. To determine if a result index is visible use the Everything_GetNumResults function.

### Example
```
FILETIME dateRun;
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the run date of the first visible result.
Everything_GetResultDateRun(0,&dateRun);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultextension

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultextension

## Everything_GetResultExtension
The Everything_GetResultExtension function retrieves the extension part of a visible result.

### Syntax
```
LPCTSTR Everything_GetResultExtension(
    DWORD dwIndex
);
```

### Parameters
dwIndex

Zero based index of the visible result.

### Return Value
The function returns a pointer to a null terminated string of TCHARs .

If the function fails the return value is NULL. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultExtension.
EVERYTHING_ERROR_INVALIDREQUEST
Extension was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_EXTENSION before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
The ANSI / Unicode version of this function must match the ANSI / Unicode version of the call to Everything_Query .

The function returns a pointer to an internal structure that is only valid until the next call to Everything_Query , Everything_Reset or Everything_CleanUp .

You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumResults function.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the extension part of the first visible result.
LPCTSTR lpExtension = Everything_GetResultExtension(0);
```

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultfilelistfilename

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultfilelistfilename

## Everything_GetResultFileListFileName
The Everything_GetResultFileListFileName function retrieves the file list full path and filename of the visible result.

### Syntax
```
LPCTSTR Everything_GetResultFileListFileName(
    DWORD dwIndex
);
```

### Parameters
dwIndex

Zero based index of the visible result.

### Return Value
The function returns a pointer to a null terminated string of TCHARs .

If the function fails the return value is NULL. To get extended error information, call Everything_GetLastError .

If the result specified by dwIndex is not in a file list, then the filename returned is an empty string.

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultFileListFileName.
EVERYTHING_ERROR_INVALIDREQUEST
The file list filename was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_FILE_LIST_FILE_NAME before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
The ANSI / Unicode version of this function must match the ANSI / Unicode version of the call to Everything_Query .

The function returns a pointer to an internal structure that is only valid until the next call to Everything_Query or Everything_Reset .

dwIndex must be a valid visible result index. To determine if a result is visible use the Everything_GetNumFileResults function.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the file list filename of the first visible result.
LPCTSTR lpFileListFileName = Everything_GetResultFileListFileName(0);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultfilename

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultfilename

## Everything_GetResultFileName
The Everything_GetResultFileName function retrieves the file name part only of the visible result.

### Syntax
```
LPCTSTR Everything_GetResultFileName(
    DWORD index
);
```

### Parameters
index

Zero based index of the visible result.

### Return Value
The function returns a pointer to a null terminated string of TCHARs .

If the function fails the return value is NULL. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultFileName.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
The ANSI / Unicode version of this function must match the ANSI / Unicode version of the call to Everything_Query .

The function is faster than Everything_GetResultFullPathName as no memory copying occurs.

The function returns a pointer to an internal structure that is only valid until the next call to Everything_Query or Everything_Reset .

You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumFileResults function.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the file name part of the first visible result.
LPCTSTR cFileName = Everything_GetResultFileName(0);
```

### See Also
- Everything_Query
- Everything_Reset
- Everything_GetResultPath
- Everything_GetResultFullPathName

## everything getresultfullpathname

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultfullpathname

## Everything_GetResultFullPathName
The Everything_GetResultFullPathName function retrieves the full path and file name of the visible result.

### Syntax
```
DWORD Everything_GetResultFullPathName(
    DWORD index,
    LPTSTR lpString,
    DWORD nMaxCount
);
```

### Parameters
index

Zero based index of the visible result.

lpString [out]

Pointer to the buffer that will receive the text. If the string is as long or longer than the buffer, the string is truncated and terminated with a NULL character.

nMaxCount

Specifies the maximum number of characters to copy to the buffer, including the NULL character. If the text exceeds this limit, it is truncated.

### Return Value
If lpString is NULL, the return value is the number of TCHARs excluding the null terminator needed to store the full path and file name of the visible result.

If lpString is not NULL, the return value is the number of TCHARs excluding the null terminator copied into lpString.

If the function fails the return value is 0. To get extended error information, call Everything_GetLastError .

Error code
Description
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultFullPathName.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumFileResults function.

You can mix ANSI / Unicode versions of Everything_GetResultFullPathName and Everything_Query.

### Example
```
TCHAR buf[MAX_PATH];
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the full path and file name of the first visible result.
Everything_GetResultFullPathName(0,buf,sizeof(buf) / sizeof(TCHAR));
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_GetResultFileName
- Everything_GetResultPath

## everything getresulthighlightedfilename

Source: https://www.voidtools.com/support/everything/sdk/everything_getresulthighlightedfilename

## Everything_GetResultHighlightedFileName
The Everything_GetResultHighlightedFileName function retrieves the highlighted file name part of the visible result.

### Syntax
```
LPCTSTR Everything_GetResultHighlightedFileName(
    int index
);
```

### Parameters
index

Zero based index of the visible result.

### Return Value
The function returns a pointer to a null terminated string of TCHARs .

If the function fails the return value is NULL. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultHighlightedFileName.
EVERYTHING_ERROR_INVALIDREQUEST
Highlighted file name information was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_DATE_HIGHLIGHTED_FILE_NAME before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
The ANSI / Unicode version of this function must match the ANSI / Unicode version of the call to Everything_Query .

The function returns a pointer to an internal structure that is only valid until the next call to Everything_Query or Everything_Reset .

You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumFileResults function.

Text inside a * quote is highlighted, two consecutive *'s is a single literal *.

For example, in the highlighted text: abc *123* the 123 part is highlighted.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the highlighted file name of the first visible result.
LPCTSTR lpHighlightedFileName = Everything_GetResultHighlightedFileName(0);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresulthighlightedfullpathandfilename

Source: https://www.voidtools.com/support/everything/sdk/everything_getresulthighlightedfullpathandfilename

## Everything_GetResultHighlightedFullPathAndFileName
The Everything_GetResultHighlightedFullPathAndFileName function retrieves the highlighted full path and file name of the visible result.

### Syntax
```
LPCTSTR Everything_GetResultHighlightedFullPathAndFileName(
    int index
);
```

### Parameters
index

Zero based index of the visible result.

### Return Value
The function returns a pointer to a null terminated string of TCHARs .

If the function fails the return value is NULL. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultHighlightedFullPathAndFileName.
EVERYTHING_ERROR_INVALIDREQUEST
Highlighted full path and file name information was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_DATE_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
The ANSI / Unicode version of this function must match the ANSI / Unicode version of the call to Everything_Query .

The function returns a pointer to an internal structure that is only valid until the next call to Everything_Query or Everything_Reset .

You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumFileResults function.

Text inside a * quote is highlighted, two consecutive *'s is a single literal *.

For example, in the highlighted text: abc *123* the 123 part is highlighted.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the highlighted full path and file name information of the first visible result.
LPCTSTR lpHighlightedFullPathAndFileName = Everything_GetResultHighlightedFullPathAndFileName(0);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresulthighlightedpath

Source: https://www.voidtools.com/support/everything/sdk/everything_getresulthighlightedpath

## Everything_GetResultHighlightedPath
The Everything_GetResultHighlightedPath function retrieves the highlighted path part of the visible result.

### Syntax
```
LPCTSTR Everything_GetResultHighlightedPath(
    int index
);
```

### Parameters
index

Zero based index of the visible result.

### Return Value
The function returns a pointer to a null terminated string of TCHARs .

If the function fails the return value is NULL. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultHighlightedPath.
EVERYTHING_ERROR_INVALIDREQUEST
Highlighted path information was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_DATE_HIGHLIGHTED_PATH before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
The ANSI / Unicode version of this function must match the ANSI / Unicode version of the call to Everything_Query .

The function returns a pointer to an internal structure that is only valid until the next call to Everything_Query or Everything_Reset .

You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumFileResults function.

Text inside a * quote is highlighted, two consecutive *'s is a single literal *.

For example, in the highlighted text: abc *123* the 123 part is highlighted.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the highlighted path of the first visible result.
LPCTSTR lpHighlightedPath = Everything_GetResultHighlightedPath(0);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultlistrequestflags

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultlistrequestflags

## Everything_GetResultListRequestFlags
The Everything_GetResultListRequestFlags function returns the flags of available result data.

### Syntax
```
DWORD Everything_GetResultListRequestFlags(void);
```

### Return Value
Returns zero or more of the following request flags:

```
EVERYTHING_REQUEST_FILE_NAME                            (0x00000001)
EVERYTHING_REQUEST_PATH                                 (0x00000002)
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME              (0x00000004)
EVERYTHING_REQUEST_EXTENSION                            (0x00000008)
EVERYTHING_REQUEST_SIZE                                 (0x00000010)
EVERYTHING_REQUEST_DATE_CREATED                         (0x00000020)
EVERYTHING_REQUEST_DATE_MODIFIED                        (0x00000040)
EVERYTHING_REQUEST_DATE_ACCESSED                        (0x00000080)
EVERYTHING_REQUEST_ATTRIBUTES                           (0x00000100)
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME                  (0x00000200)
EVERYTHING_REQUEST_RUN_COUNT                            (0x00000400)
EVERYTHING_REQUEST_DATE_RUN                             (0x00000800)
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED                (0x00001000)
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME                (0x00002000)
EVERYTHING_REQUEST_HIGHLIGHTED_PATH                     (0x00004000)
EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME  (0x00008000)
```

### Remarks
The requested result data may differ to the desired result data specified in Everything_SetRequestFlags .

### Example
```
DWORD dwRequestFlags = Everything_GetResultListRequestFlags();
```

### See Also
- Everything_SetRequestFlags
- Everything_Query

## everything getresultlistsort

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultlistsort

## Everything_GetResultListSort
The Everything_GetResultListSort function returns the actual sort order for the results.

### Syntax
```
DWORD Everything_GetResultListSort(void);
```

### Return Value
Returns one of the following sort types:

```
EVERYTHING_SORT_NAME_ASCENDING                      (1)
EVERYTHING_SORT_NAME_DESCENDING                     (2)
EVERYTHING_SORT_PATH_ASCENDING                      (3)
EVERYTHING_SORT_PATH_DESCENDING                     (4)
EVERYTHING_SORT_SIZE_ASCENDING                      (5)
EVERYTHING_SORT_SIZE_DESCENDING                     (6)
EVERYTHING_SORT_EXTENSION_ASCENDING                 (7)
EVERYTHING_SORT_EXTENSION_DESCENDING                (8)
EVERYTHING_SORT_TYPE_NAME_ASCENDING                 (9)
EVERYTHING_SORT_TYPE_NAME_DESCENDING                (10)
EVERYTHING_SORT_DATE_CREATED_ASCENDING              (11)
EVERYTHING_SORT_DATE_CREATED_DESCENDING             (12)
EVERYTHING_SORT_DATE_MODIFIED_ASCENDING             (13)
EVERYTHING_SORT_DATE_MODIFIED_DESCENDING            (14)
EVERYTHING_SORT_ATTRIBUTES_ASCENDING                (15)
EVERYTHING_SORT_ATTRIBUTES_DESCENDING               (16)
EVERYTHING_SORT_FILE_LIST_FILENAME_ASCENDING        (17)
EVERYTHING_SORT_FILE_LIST_FILENAME_DESCENDING       (18)
EVERYTHING_SORT_RUN_COUNT_ASCENDING                 (19)
EVERYTHING_SORT_RUN_COUNT_DESCENDING                (20)
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_ASCENDING     (21)
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_DESCENDING    (22)
EVERYTHING_SORT_DATE_ACCESSED_ASCENDING             (23)
EVERYTHING_SORT_DATE_ACCESSED_DESCENDING            (24)
EVERYTHING_SORT_DATE_RUN_ASCENDING                  (25)
EVERYTHING_SORT_DATE_RUN_DESCENDING                 (26)
```

### Remarks
Everything_GetResultListSort must be called after calling Everything_Query .

If no desired sort order was specified the result list is sorted by EVERYTHING_SORT_NAME_ASCENDING.

The result list sort may differ to the desired sort specified in Everything_SetSort .

### Example
```
DWORD dwSort = Everything_GetResultListSort();
```

### See Also
- Everything_SetSort
- Everything_Query

## everything getresultpath

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultpath

## Everything_GetResultPath
The Everything_GetResultPath function retrieves the path part of the visible result.

### Syntax
```
LPCTSTR Everything_GetResultPath(
    int index
);
```

### Parameters
index

Zero based index of the visible result.

### Return Value
The function returns a pointer to a null terminated string of TCHARs .

If the function fails the return value is NULL. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultPath.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
The ANSI / Unicode version of this function must match the ANSI / Unicode version of the call to Everything_Query .

The function is faster than Everything_GetResultFullPathName as no memory copying occurs.

The function returns a pointer to an internal structure that is only valid until the next call to Everything_Query or Everything_Reset .

You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumFileResults function.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the path part of the first visible result.
LPCTSTR lpPath = Everything_GetResultPath(0);
```

### See Also
- Everything_Query
- Everything_Reset
- Everything_GetResultFileName
- Everything_GetResultFullPathName

## everything getresultruncount

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultruncount

## Everything_GetResultRunCount
The Everything_GetResultRunCount function retrieves the number of times a visible result has been run from Everything.

### Syntax
```
DWORD Everything_GetResultRunCount(
    DWORD dwIndex,
);
```

### Parameters
dwIndex

Zero based index of the visible result.

### Return Value
The function returns the number of times the result has been run from Everything.

The function returns 0 if the run count information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_OK
The run count is 0.
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultRunCount.
EVERYTHING_ERROR_INVALIDREQUEST
Run count information was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_RUN_COUNT before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
dwIndex must be a valid visible result index. To determine if a result index is visible use the Everything_GetNumResults function.

### Example
```
DWORD runCount;
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the run count of the first visible result.
runCount = Everything_GetResultRunCount(0);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getresultsize

Source: https://www.voidtools.com/support/everything/sdk/everything_getresultsize

## Everything_GetResultSize
The Everything_GetResultSize function retrieves the size of a visible result.

### Syntax
```
BOOL Everything_GetResultSize(
    DWORD dwIndex,
    LARGE_INTEGER *lpSize
);
```

### Parameters
dwIndex

Zero based index of the visible result.

lpSize

Pointer to a LARGE_INTEGER to hold the size of the result.

### Return Value
The function returns non-zero if successful.

The function returns 0 if size information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetResultSize.
EVERYTHING_ERROR_INVALIDREQUEST
Size was not requested or is unavailable, Call 
Everything_SetRequestFlags
 with EVERYTHING_REQUEST_SIZE before calling 
Everything_Query
.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
dwIndex must be a valid visible result index. To determine if a result index is visible use the Everything_GetNumResults function.

### Example
```
LARGE_INTEGER size;
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// Get the size of the first visible result.
Everything_GetResultSize(0,&size);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_Reset
- Everything_SetRequestFlags

## everything getrevision

Source: https://www.voidtools.com/support/everything/sdk/everything_getrevision

## Everything_GetRevision
The Everything_GetRevision function retrieves the revision number of Everything.

### Syntax
```
DWORD Everything_GetRevision(void);
```

### Parameters
No parameters.

### Return Value
The function returns the revision number.

The function returns 0 if revision information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Everything uses the following version format:

major.minor.revision.build

The build part is incremental and unique for all Everything versions.

### Example
```
DWORD majorVersion;
DWORD minorVersion;
DWORD revision;
// get version information
majorVersion = Everything_GetMajorVersion();
minorVersion = Everything_GetMinorVersion();
revision = Everything_GetRevision();
if ((majorVersion > 1) || ((majorVersion == 1) && (minorVersion > 3)) || ((majorVersion == 1) && (minorVersion == 3) && (revision >= 4)))
{
	// do something with version 1.3.4 or later
}
```

### Function Information
Requires Everything 1.0.0.0 or later.

### See Also
- Everything_GetMajorVersion
- Everything_GetMinorVersion
- Everything_GetBuildNumber
- Everything_GetTargetMachine

## everything getruncountfromfilename

Source: https://www.voidtools.com/support/everything/sdk/everything_getruncountfromfilename

## Everything_GetRunCountFromFileName
The Everything_GetRunCountFromFileName function gets the run count from a specified file in the Everything index by file name.

### Syntax
```
DWORD Everything_GetRunCountFromFileName(
    LPCTSTR lpFileName
);
```

### Parameters
lpFileName [in]

Pointer to a null-terminated string that specifies a fully qualified file name in the Everything index.

### Return Value
The function returns the number of times the file has been run from Everything.

The function returns 0 if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_OK
The run count is 0.
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
### Example
```
DWORD runCount;
// get the run count of a file.
runCount = Everything_GetRunCountFromFileName(TEXT("C:\\folder\\file.doc"));
```

### See Also
- Everything_SetRunCountFromFileName
- Everything_IncRunCountFromFileName

## everything getsearch

Source: https://www.voidtools.com/support/everything/sdk/everything_getsearch

## Everything_GetSearch
The Everything_GetSearch function retrieves the search text to use for the next call to Everything_Query .

### Syntax
```
LPCTSTR Everything_GetSearch(void);
```

### Return Value
The return value is a pointer to the null terminated search string.

The unicode and ansi version must match the call to Everything_SetSearch.

The function will fail if you call Everything_GetSearchA after a call to Everything_SetSearchW

The function will fail if you call Everything_GetSearchW after a call to Everything_SetSearchA

If the function fails, the return value is NULL.

To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Mismatched unicode / ansi call. 
### Remarks
Get the internal state of the search text.

The default string is an empty string.

### Example
```
LPCTSTR lpSearchString = Everything_GetSearch();
```

### See Also
- Everything_SetSearch
- Everything_Query

## everything getsort

Source: https://www.voidtools.com/support/everything/sdk/everything_getsort

## Everything_GetSort
The Everything_GetSort function returns the desired sort order for the results.

### Syntax
```
DWORD Everything_GetSort(void);
```

### Return Value
Returns one of the following sort types:

```
EVERYTHING_SORT_NAME_ASCENDING                      (1)
EVERYTHING_SORT_NAME_DESCENDING                     (2)
EVERYTHING_SORT_PATH_ASCENDING                      (3)
EVERYTHING_SORT_PATH_DESCENDING                     (4)
EVERYTHING_SORT_SIZE_ASCENDING                      (5)
EVERYTHING_SORT_SIZE_DESCENDING                     (6)
EVERYTHING_SORT_EXTENSION_ASCENDING                 (7)
EVERYTHING_SORT_EXTENSION_DESCENDING                (8)
EVERYTHING_SORT_TYPE_NAME_ASCENDING                 (9)
EVERYTHING_SORT_TYPE_NAME_DESCENDING                (10)
EVERYTHING_SORT_DATE_CREATED_ASCENDING              (11)
EVERYTHING_SORT_DATE_CREATED_DESCENDING             (12)
EVERYTHING_SORT_DATE_MODIFIED_ASCENDING             (13)
EVERYTHING_SORT_DATE_MODIFIED_DESCENDING            (14)
EVERYTHING_SORT_ATTRIBUTES_ASCENDING                (15)
EVERYTHING_SORT_ATTRIBUTES_DESCENDING               (16)
EVERYTHING_SORT_FILE_LIST_FILENAME_ASCENDING        (17)
EVERYTHING_SORT_FILE_LIST_FILENAME_DESCENDING       (18)
EVERYTHING_SORT_RUN_COUNT_ASCENDING                 (19)
EVERYTHING_SORT_RUN_COUNT_DESCENDING                (20)
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_ASCENDING     (21)
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_DESCENDING    (22)
EVERYTHING_SORT_DATE_ACCESSED_ASCENDING             (23)
EVERYTHING_SORT_DATE_ACCESSED_DESCENDING            (24)
EVERYTHING_SORT_DATE_RUN_ASCENDING                  (25)
EVERYTHING_SORT_DATE_RUN_DESCENDING                 (26)
```

### Remarks
The default sort is EVERYTHING_SORT_NAME_ASCENDING (1)

### Example
```
DWORD dwSort = Everything_GetSort();
```

### See Also
- Everything_SetSort
- Everything_Query

## everything gettargetmachine

Source: https://www.voidtools.com/support/everything/sdk/everything_gettargetmachine

## Everything_GetTargetMachine
The Everything_GetTargetMachine function retrieves the target machine of Everything.

### Syntax
```
DWORD Everything_GetTargetMachine(void);
```

### Parameters
No parameters.

### Return Value
The function returns one of the following:

Macro
Meaning
EVERYTHING_TARGET_MACHINE_X86 (1)
Target machine is x86 (32 bit).
EVERYTHING_TARGET_MACHINE_X64 (2)
Target machine is x64 (64 bit).
EVERYTHING_TARGET_MACHINE_ARM (3)
Target machine is ARM.
EVERYTHING_TARGET_MACHINE_ARM64 (4)
Target machine is ARM64.
The function returns 0 if target machine information is unavailable. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Everything uses the following version format:

major.minor.revision.build

The build part is incremental and unique for all Everything versions.

### Example
```
DWORD targetMachine;
// Get the attributes of the first visible result.
targetMachine = Everything_GetTargetMachine();
if (targetMachine == EVERYTHING_TARGET_MACHINE_X64)
{
	// do something with x64 build.
}
else
if (targetMachine == EVERYTHING_TARGET_MACHINE_X86)
{
	// do something with x86 build.
}
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_GetMajorVersion
- Everything_GetMinorVersion
- Everything_GetRevision
- Everything_GetBuildNumber

## everything gettotfileresults

Source: https://www.voidtools.com/support/everything/sdk/everything_gettotfileresults

## Everything_GetTotFileResults
The Everything_GetTotFileResults function returns the total number of file results.

### Syntax
```
DWORD Everything_GetTotFileResults(void);
```

### Parameters
This functions has no parameters.

### Return Value
Returns the total number of file results.

If the function fails the return value is 0. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetTotFileResults.
### Remarks
You must call Everything_Query before calling Everything_GetTotFileResults.

Use Everything_GetNumFileResults to retrieve the number of visible file results.

Use the result offset and max result values to limit the number of visible results.

Everything_GetTotFileResults is not supported when using Everything_SetRequestFlags

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// get the total number of file results.
DWORD dwTotFileResults = Everything_GetTotFileResults();
```

### See Also
- Everything_Query
- Everything_GetNumResults
- Everything_GetNumFileResults
- Everything_GetNumFolderResults
- Everything_GetTotResults
- Everything_GetTotFolderResults

## everything gettotfolderresults

Source: https://www.voidtools.com/support/everything/sdk/everything_gettotfolderresults

## Everything_GetTotFolderResults
The Everything_GetTotFolderResults function returns the total number of folder results.

### Syntax
```
DWORD Everything_GetTotFolderResults(void);
```

### Parameters
This functions has no parameters.

### Return Value
Returns the total number of folder results.

If the function fails the return value is 0. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetTotFolderResults.
### Remarks
You must call Everything_Query before calling Everything_GetTotFolderResults.

Use Everything_GetNumFolderResults to retrieve the number of visible folder results.

Use the result offset and max result values to limit the number of visible results.

Everything_GetTotFolderResults is not supported when using Everything_SetRequestFlags

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// get the total number of folder results.
DWORD dwTotFolderResults = Everything_GetTotFolderResults();
```

### See Also
- Everything_Query
- Everything_GetNumResults
- Everything_GetNumFileResults
- Everything_GetNumFolderResults
- Everything_GetTotResults
- Everything_GetTotFileResults

## everything gettotresults

Source: https://www.voidtools.com/support/everything/sdk/everything_gettotresults

## Everything_GetTotResults
The Everything_GetTotResults function returns the total number of file and folder results.

### Syntax
```
DWORD Everything_GetTotResults(void);
```

### Parameters
This functions has no parameters.

### Return Value
Returns the total number of file and folder results.

If the function fails the return value is 0. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_GetTotResults.
### Remarks
You must call Everything_Query before calling Everything_GetTotResults.

Use Everything_GetNumResults to retrieve the number of visible file and folder results.

Use the result offset and max result values to limit the number of visible results.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// get the total number of file and folder results.
DWORD dwTotResults = Everything_GetTotResults();
```

### See Also
- Everything_Query
- Everything_GetNumResults
- Everything_GetNumFileResults
- Everything_GetNumFolderResults
- Everything_GetTotFileResults
- Everything_GetTotFolderResults

## everything incruncountfromfilename

Source: https://www.voidtools.com/support/everything/sdk/everything_incruncountfromfilename

## Everything_IncRunCountFromFileName
The Everything_IncRunCountFromFileName function increments the run count by one for a specified file in the Everything by file name.

### Syntax
```
DWORD Everything_IncRunCountFromFileName(
    LPCTSTR lpFileName
);
```

### Parameters
lpFileName [in]

Pointer to a null-terminated string that specifies a fully qualified file name in the Everything index.

### Return Value
The function returns the new run count for the specifed file.

The function returns 0 if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
The file does not have to exist. When the file is created it will have the correct run history.

Run history information is preserved between file deletion and creation.

Calling this function will update the date run to the current time for the specified file.

Incrementing a file with a run count of 4294967295 (0xffffffff) will do nothing.

### Example
```
// run a file
system("C:\\folder\\file.doc");
// increment the run count in Everything.
Everything_IncRunCountFromFileName(TEXT("C:\\folder\\file.doc"));
```

### See Also
- Everything_GetRunCountFromFileName
- Everything_SetRunCountFromFileName

## everything isadmin

Source: https://www.voidtools.com/support/everything/sdk/everything_isadmin

## Everything_IsAdmin
The Everything_IsAdmin function checks if Everything is running as administrator or as a standard user.

### Syntax
```
BOOL Everything_IsAdmin(void);
```

### Parameters
No parameters.

### Return Value
The function returns non-zero if the Everything is running as an administrator.

The function returns 0 Everything is running as a standard user or if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_OK
Everything is running as a standard user.
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
### Example
```
BOOL isAdmin;
isAdmin = Everything_IsAdmin();
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_IsAppData

## everything isappdata

Source: https://www.voidtools.com/support/everything/sdk/everything_isappdata

## Everything_IsAppData
The Everything_IsAppData function checks if Everything is saving settings and data to %APPDATA%\Everything or to the same location as the Everything.exe.

### Syntax
```
BOOL Everything_IsAppData(void);
```

### Parameters
No parameters.

### Return Value
The function returns non-zero if settings and data are saved in %APPDATA%\Everything.

The function returns 0 if settings and data are saved to the same location as the Everything.exe or if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_OK
Settings and data are stored in the same location as the Everything.exe.
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
### Example
```
BOOL isAppData;
isAppData = Everything_IsAppData();
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_IsAdmin

## everything isdbloaded

Source: https://www.voidtools.com/support/everything/sdk/everything_isdbloaded

## Everything_IsDBLoaded
The Everything_IsDBLoaded function checks if the database has been fully loaded.

### Syntax
```
BOOL Everything_IsDBLoaded(void);
```

### Parameters
No parameters.

### Return Value
The function returns non-zero if the Everything database is fully loaded.

The function returns 0 if the database has not fully loaded or if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_OK
The database is still loading.
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
When Everything is loading, any queries will appear to return no results.

Use Everything_IsDBLoaded to determine if the database has been loaded before performing a query.

### Example
```
for(;;)
{
	if (Everything_IsDBLoaded())
	{
		// perform a query...
		break;
	}	
	else
	{
		if (Everything_GetLastError())
		{
			// IPC not running.
			break;
		}
	}
	
	// wait for database to load..
	Sleep(1000);
}
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query

## everything isfastsort

Source: https://www.voidtools.com/support/everything/sdk/everything_isfastsort

## Everything_IsFastSort
The Everything_IsFastSort function checks if the specified file information is indexed and has fast sort enabled.

### Syntax
```
BOOL Everything_IsFastSort(DWORD sortType);
```

### Parameters
sortType

Can be one of the following:

Code
Value
Description
EVERYTHING_IPC_SORT_NAME_ASCENDING
1
Name ascending
EVERYTHING_IPC_SORT_NAME_DESCENDING 
2
Name descending
EVERYTHING_IPC_SORT_PATH_ASCENDING 
3
Path ascending
EVERYTHING_IPC_SORT_PATH_DESCENDING 
4
Path descending
EVERYTHING_IPC_SORT_SIZE_ASCENDING 
5
Size ascending
EVERYTHING_IPC_SORT_SIZE_DESCENDING 
6
Size descending
EVERYTHING_IPC_SORT_EXTENSION_ASCENDING 
7
Extension ascending
EVERYTHING_IPC_SORT_EXTENSION_DESCENDING 
8
Extension descending
EVERYTHING_IPC_SORT_TYPE_NAME_ASCENDING 
9
Type name ascending
EVERYTHING_IPC_SORT_TYPE_NAME_DESCENDING 
10
Type name descending
EVERYTHING_IPC_SORT_DATE_CREATED_ASCENDING 
11
Date created ascending
EVERYTHING_IPC_SORT_DATE_CREATED_DESCENDING 
12
Date created descending
EVERYTHING_IPC_SORT_DATE_MODIFIED_ASCENDING 
13
Date modified ascending
EVERYTHING_IPC_SORT_DATE_MODIFIED_DESCENDING 
14
Date modified descending
EVERYTHING_IPC_SORT_ATTRIBUTES_ASCENDING 
15
Attributes ascending
EVERYTHING_IPC_SORT_ATTRIBUTES_DESCENDING 
16
Attributes descending
EVERYTHING_IPC_SORT_FILE_LIST_FILENAME_ASCENDING 
17
File list filename ascending
EVERYTHING_IPC_SORT_FILE_LIST_FILENAME_DESCENDING 
18
File list filename descending
EVERYTHING_IPC_SORT_RUN_COUNT_ASCENDING 
19
Run count ascending
EVERYTHING_IPC_SORT_RUN_COUNT_DESCENDING 
20
Run count descending
EVERYTHING_IPC_SORT_DATE_RECENTLY_CHANGED_ASCENDING
21
Recently changed ascending
EVERYTHING_IPC_SORT_DATE_RECENTLY_CHANGED_DESCENDING
22
Recently changed descending
EVERYTHING_IPC_SORT_DATE_ACCESSED_ASCENDING
23
Date accessed ascending
EVERYTHING_IPC_SORT_DATE_ACCESSED_DESCENDING
24
Date accessed descending
EVERYTHING_IPC_SORT_DATE_RUN_ASCENDING
25
Date run ascending
EVERYTHING_IPC_SORT_DATE_RUN_DESCENDING
26
Date run descending
### Return Value
The function returns non-zero if the specified information is indexed and has fast sort enabled.

The function returns 0 if the specified information does not have fast sort enabled or if an error occurred. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_OK
The specified information does not have fast sort enabled.
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
The following sort types are always fast sort types:

Code
Value
Description
EVERYTHING_IPC_SORT_NAME_ASCENDING
1
Name ascending
EVERYTHING_IPC_SORT_NAME_DESCENDING 
2
Name descending
EVERYTHING_IPC_SORT_RUN_COUNT_ASCENDING 
19
Run count ascending
EVERYTHING_IPC_SORT_RUN_COUNT_DESCENDING 
20
Run count descending
EVERYTHING_IPC_SORT_DATE_RECENTLY_CHANGED_ASCENDING
21
Recently changed ascending
EVERYTHING_IPC_SORT_DATE_RECENTLY_CHANGED_DESCENDING
22
Recently changed descending
EVERYTHING_IPC_SORT_DATE_RUN_ASCENDING
25
Date run ascending
EVERYTHING_IPC_SORT_DATE_RUN_DESCENDING
26
Date run descending
### Example
```
BOOL isFastSizeSort;
// Check if sorting by size descending will be instant.
isFastSizeSort = Everything_IsFastSort(EVERYTHING_IPC_SORT_SIZE_DESCENDING);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_IsFileInfoIndexed
- Enable or disable file information indexing
- Enable or disable fast sorting

## everything isfileinfoindexed

Source: https://www.voidtools.com/support/everything/sdk/everything_isfileinfoindexed

## Everything_IsFileInfoIndexed
The Everything_IsFileInfoIndexed function checks if the specified file information is indexed.

### Syntax
```
BOOL Everything_IsFileInfoIndexed(DWORD fileInfoType);
```

### Parameters
fileInfoType

Can be one of the following:

Code
Value
Description
EVERYTHING_IPC_FILE_INFO_FILE_SIZE
1
File size
EVERYTHING_IPC_FILE_INFO_FOLDER_SIZE
2
Folder size
EVERYTHING_IPC_FILE_INFO_DATE_CREATED
3
Date created
EVERYTHING_IPC_FILE_INFO_DATE_MODIFIED
4
Date modified
EVERYTHING_IPC_FILE_INFO_DATE_ACCESSED
5
Date accessed
EVERYTHING_IPC_FILE_INFO_ATTRIBUTES
6
Attributes
### Return Value
The function returns non-zero if the specified information is indexed.

The function returns 0 if the specified information is not indexed or if an error occurred. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_OK
The specified information is not indexed.
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
### Example
```
BOOL isSizeIndexed;
isSizeIndexed = Everything_IsFileInfoIndexed(EVERYTHING_IPC_FILE_INFO_FILE_SIZE);
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_IsFastSort
- Enable or disable file information indexing
- Enable or disable fast sorting

## everything isfileresult

Source: https://www.voidtools.com/support/everything/sdk/everything_isfileresult

## Everything_IsFileResult
The Everything_IsFileResult function determines if the visible result is file.

### Syntax
```
BOOL Everything_IsFileResult(
    DWORD index
);
```

### Parameters
index

Zero based index of the visible result.

### Return Value
The function returns TRUE, if the visible result is a file (For example: C:\ABC.123).

The function returns FALSE, if the visible result is a folder or volume (For example: C: or c:\WINDOWS).

If the function fails the return value is FALSE. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_IsFileResult.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumFileResults function.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// determine if the first visible result is a file.
BOOL bIsFileResult = Everything_IsFileResult(0);
```

### See Also
- Everything_Query
- Everything_IsVolumeResult
- Everything_IsFolderResult

## everything isfolderresult

Source: https://www.voidtools.com/support/everything/sdk/everything_isfolderresult

## Everything_IsFolderResult
The Everything_IsFolderResult function determines if the visible result is a folder.

### Syntax
```
BOOL Everything_IsFolderResult(
    DWORD index
);
```

### Parameters
index

Zero based index of the visible result.

### Return Value
The function returns TRUE, if the visible result is a folder or volume (For example: C: or c:\WINDOWS).

The function returns FALSE, if the visible result is a file (For example: C:\ABC.123).

If the function fails the return value is FALSE. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_IsFolderResult.
EVERYTHING_ERROR_INVALIDINDEX
Index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumFileResults function.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// determine if the first visible result is a folder.
BOOL bIsFolderResult = Everything_IsFolderResult(0);
```

### See Also
- Everything_Query
- Everything_IsVolumeResult
- Everything_IsFileResult

## everything isqueryreply

Source: https://www.voidtools.com/support/everything/sdk/everything_isqueryreply

## Everything_IsQueryReply
The Everything_IsQueryReply function checks if the specified window message is a query reply.

### Syntax
```
BOOL EVERYTHINGAPI Everything_IsQueryReply(
    UINT message,
    WPARAM wParam,
    LPARAM lParam,
    DWORD nId
);
```

### Parameters
message

Specifies the message identifier.

wParam

Specifies additional information about the message.

lParam

Specifies additional information about the message.

nId

The unique identifier specified with Everything_SetReplyID , or 0 for the default ID.

This is the value used to compare with the dwData member of the COPYDATASTRUCT if the message is WM_COPYDATA.

### Return Value
Returns TRUE if the message is a query reply.

If the function fails the return value is FALSE. To get extended error information, call: Everything_GetLastError .

### Remarks
This function checks if the message is a WM_COPYDATA message. If the message is a WM_COPYDATA message the function checks if the ReplyID matches the dwData member of the COPYDATASTRUCT. If they match the function makes a copy of the query results.

You must call Everything_IsQueryReply in the windows message handler to check for an IPC query reply if you call Everything_Query with bWait set to FALSE.

If the function returns TRUE you should return TRUE.

If the function returns TRUE you can call the following functions to read the results:

- Everything_SortResultsByPath
- Everything_Reset
- Everything_GetNumFileResults
- Everything_GetNumFolderResults
- Everything_GetNumResults
- Everything_GetTotFileResults
- Everything_GetTotFolderResults
- Everything_GetTotResults
- Everything_IsVolumeResult
- Everything_IsFolderResult
- Everything_IsFileResult
- Everything_GetResultFileName
- Everything_GetResultPath
- Everything_GetResultFullPathName

### Example
```
LRESULT CALLBACK WindowProc(HWND hwnd,UINT uMsg,WPARAM wParam,LPARAM lParam)
{
	if (Everything_IsQueryReply(uMsg,wParam,lParam,0))
	{
		// ...
		// do something with the results..
		// ...
		
		return TRUE;
	}
	// return the default window proc..
	return DefWindowProc(hwnd,uMsg,wParam,lParam);
}
```

### Implementation
```
BOOL EVERYTHINGAPI Everything_IsQueryReply(UINT message,WPARAM wParam,LPARAM lParam,DWORD nId)
{
	if (message == WM_COPYDATA)
	{
		COPYDATASTRUCT *cds = (COPYDATASTRUCT *)lParam;
		
		if (cds)
		{
			if (cds->dwData == _Everything_ReplyID)
			{
				if (_Everything_IsUnicodeQuery)				
				{
					if (_Everything_List) HeapFree(GetProcessHeap(),0,_Everything_List);
					
					_Everything_List = (EVERYTHING_IPC_LISTW *)HeapAlloc(GetProcessHeap(),0,cds->cbData);
					
					if (_Everything_List)
					{
						CopyMemory(_Everything_List,cds->lpData,cds->cbData);
					}
					else
					{
						_Everything_LastError = EVERYTHING_ERROR_MEMORY;
					}
					
					return TRUE;
				}
				else
				{
					if (_Everything_List) HeapFree(GetProcessHeap(),0,_Everything_List);
					
					_Everything_List = (EVERYTHING_IPC_LISTW *)HeapAlloc(GetProcessHeap(),0,cds->cbData);
					
					if (_Everything_List)
					{
						CopyMemory(_Everything_List,cds->lpData,cds->cbData);
					}
					else
					{
						_Everything_LastError = EVERYTHING_ERROR_MEMORY;
					}
					
					return TRUE;
				}
			}
		}
	}
	
	return FALSE;
}
```

### See Also
- Everything_Query
- Everything_SetReplyWindow
- Everything_SetReplyID
- Everything_GetReplyWindow
- Everything_GetReplyID

## everything isvolumeresult

Source: https://www.voidtools.com/support/everything/sdk/everything_isvolumeresult

## Everything_IsVolumeResult
The Everything_IsVolumeResult function determines if the visible result is the root folder of a volume.

### Syntax
```
BOOL Everything_IsVolumeResult(
    DWORD index
);
```

### Parameters
index

Zero based index of the visible result.

### Return Value
The function returns TRUE, if the visible result is a volume (For example: C:).

The function returns FALSE, if the visible result is a folder or file (For example: C:\ABC.123).

If the function fails the return value is FALSE. To get extended error information, call Everything_GetLastError .

Error code
Meaning
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_Query
 before calling Everything_IsVolumeResult.
EVERYTHING_ERROR_INVALIDINDEX
index must be greater than or equal to 0 and less than the visible number of results.
### Remarks
You can only call this function for a visible result. To determine if a result is visible use the Everything_GetNumFileResults function.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// execute the query
Everything_Query(TRUE);
// determine if the first visible result is a volume.
BOOL bIsVolumeResult = Everything_IsVolumeResult(0);
```

### See Also
- Everything_Query
- Everything_IsFolderResult
- Everything_IsFileResult

## everything query

Source: https://www.voidtools.com/support/everything/sdk/everything_query

## Everything_Query
The Everything_Query function executes an Everything IPC query with the current search state.

### Syntax
```
BOOL Everything_Query(
    BOOL bWait
);
```

### Parameters
bWait

Should the function wait for the results or return immediately.

Set this to FALSE to post the IPC Query and return immediately.

Set this to TRUE to send the IPC Query and wait for the results.

### Return Value
If the function succeeds, the return value is TRUE.

If the function fails, the return value is FALSE.  To get extended error information, call Everything_GetLastError

Error code
Description
EVERYTHING_ERROR_CREATETHREAD
Failed to create the search query thread. 
EVERYTHING_ERROR_REGISTERCLASSEX
Failed to register the search query window class.
EVERYTHING_ERROR_CREATEWINDOW
Failed to create the search query window.
EVERYTHING_ERROR_IPC
IPC is not available. Make sure Everything is running.
EVERYTHING_ERROR_MEMORY
Failed to allocate memory for the search query.
EVERYTHING_ERROR_INVALIDCALL
Call 
Everything_SetReplyWindow
 before calling Everything_Query with bWait set to FALSE.
### Remarks
If bWait is FALSE you must call Everything_SetReplyWindow before calling Everything_Query. Use the Everything_IsQueryReply function to check for query replies.

Optionally call the following functions to set the search state before calling Everything_Query:

- Everything_SetSearch
- Everything_SetMatchPath
- Everything_SetMatchCase
- Everything_SetMatchWholeWord
- Everything_SetRegex
- Everything_SetMax
- Everything_SetOffset
- Everything_SetReplyID
- Everything_SetRequestFlags

You can mix ANSI / Unicode version of Everything_SetSearch and Everything_Query.

The ANSI / Unicode version of Everything_Query MUST match the ANSI / Unicode version of Everything_GetResultName and Everything_GetResultPath.

The search state is not modified from a call to Everything_Query.

The default state is as follows:

See Everything_Reset for the default search state.

### Example
```
// set the search text to abc AND 123
Everything_SetSearch("abc 123");
// enable case sensitive searching.
Everything_SetMatchCase(TRUE);
// execute the query
Everything_Query(TRUE);
```

### See Also
- Everything_SetSearch
- Everything_SetMatchPath
- Everything_SetMatchCase
- Everything_SetMatchWholeWord
- Everything_SetRegex
- Everything_SetMax
- Everything_SetOffset
- Everything_SortResultsByPath
- Everything_GetLastError
- Everything_GetNumFileResults
- Everything_GetNumFolderResults
- Everything_GetNumResults
- Everything_GetTotFileResults
- Everything_GetTotFolderResults
- Everything_GetTotResults
- Everything_IsVolumeResult
- Everything_IsFolderResult
- Everything_IsFileResult
- Everything_GetResultFileName
- Everything_GetResultPath
- Everything_GetResultFullPathName
- Everything_SetReplyWindow
- Everything_SetReplyID
- Everything_Reset

## everything rebuilddb

Source: https://www.voidtools.com/support/everything/sdk/everything_rebuilddb

## Everything_RebuildDB
The Everything_RebuildDB function requests Everything to forcefully rebuild the Everything index.

### Syntax
```
BOOL Everything_RebuildDB(void);
```

### Parameters
No parameters.

### Return Value
The function returns non-zero if the request to forcefully rebuild the Everything index was successful.

The function returns 0 if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Requesting a rebuild will mark all indexes as dirty and start the rebuild process.

Use Everything_IsDBLoaded to determine if the database has been rebuilt before performing a query.

### Example
```
// rebuild the database.
Everything_RebuildDB();
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also
- Everything_IsDBLoaded

## everything reset

Source: https://www.voidtools.com/support/everything/sdk/everything_reset

## Everything_Reset
The Everything_Reset function resets the result list and search state to the default state, freeing any allocated memory by the library.

### Syntax
```
void Everything_Reset(void);
```

### Parameters
This function has no parameters.

### Return Value
This function has no return value.

### Remarks
Calling Everything_SetSearch frees the old search and allocates the new search string.

Calling Everything_Query frees the old result list and allocates the new result list.

Calling Everything_Reset frees the current search and current result list.

The default state:

```
Everything_SetSearch(\"\");
Everything_SetMatchPath(FALSE);
Everything_SetMatchCase(FALSE);
Everything_SetMatchWholeWord(FALSE);
Everything_SetRegex(FALSE);
Everything_SetMax(0xFFFFFFFF);
Everything_SetOffset(0);
Everything_SetReplyWindow(0);
Everything_SetReplyID(0);
```

### Example
```
Everything_Reset();
```

### See Also
- Everything_SetSearch
- Everything_Query
- Everything_CleanUp

## everything savedb

Source: https://www.voidtools.com/support/everything/sdk/everything_savedb

## Everything_SaveDB
The Everything_SaveDB function requests Everything to save the index to disk.

### Syntax
```
BOOL Everything_SaveDB(void);
```

### Parameters
No parameters.

### Return Value
The function returns non-zero if the request to save the Everything index to disk was successful.

The function returns 0 if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
The index is only saved to disk when you exit Everything.

Call Everything_SaveDB to write the index to the file: Everything.db

### Example
```
// flush index to disk
Everything_SaveDB();
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also

## everything saverunhistory

Source: https://www.voidtools.com/support/everything/sdk/everything_saverunhistory

## Everything_SaveRunHistory
The Everything_SaveRunHistory function requests Everything to save the run history to disk.

### Syntax
```
BOOL Everything_SaveRunHistory(void);
```

### Parameters
No parameters.

### Return Value
The function returns non-zero if the request to save the run history to disk was successful.

The function returns 0 if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
The run history is only saved to disk when you close an Everything search window or exit Everything.

Call Everything_RunHistory to write the run history to the file: Run History.csv

### Example
```
// flush run history to disk
Everything_SaveRunHistory();
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also

## everything setmatchcase

Source: https://www.voidtools.com/support/everything/sdk/everything_setmatchcase

## Everything_SetMatchCase
The Everything_SetMatchCase function enables or disables full path matching for the next call to Everything_Query .

### Syntax
```
void Everything_SetMatchCase(
    BOOL bEnable
);
```

### Parameters
bEnable

Specifies whether the search is case sensitive or insensitive.

If this parameter is TRUE, the search is case sensitive.

If the parameter is FALSE, the search is case insensitive.

### Remarks
Match case is disabled by default.

### Example
```
Everything_SetMatchCase(TRUE);
```

### See Also
- Everything_GetMatchCase
- Everything_Query

## everything setmatchpath

Source: https://www.voidtools.com/support/everything/sdk/everything_setmatchpath

## Everything_SetMatchPath
The Everything_SetMatchPath function enables or disables full path matching for the next call to Everything_Query .

### Syntax
```
void Everything_SetMatchPath(
    BOOL bEnable
);
```

### Parameters
bEnable

[in] Specifies whether to enable or disable full path matching.

If this parameter is TRUE, full path matching is enabled.

If the parameter is FALSE, full path matching is disabled.

### Remarks
If match full path is being enabled, the next call to Everything_Query will search the full path and file name of each file and folder.

If match full path is being disabled, the next call to Everything_Query will search the file name only of each file and folder.

Match path is disabled by default.

Enabling match path will add a significant performance hit.

### Example
```
Everything_SetMatchPath(TRUE);
```

### See Also
- Everything_GetMatchPath
- Everything_Query

## everything setmatchwholeword

Source: https://www.voidtools.com/support/everything/sdk/everything_setmatchwholeword

## Everything_SetMatchWholeWord
The Everything_SetMatchWholeWord function enables or disables matching whole words for the next call to Everything_Query .

### Syntax
```
void Everything_SetMatchWholeWord(
    BOOL bEnable
);
```

### Parameters
bEnable

Specifies whether the search matches whole words, or can match anywhere.

If this parameter is TRUE, the search matches whole words only.

If the parameter is FALSE, the search can occur anywhere.

### Remarks
Match whole word is disabled by default.

### Example
```
Everything_SetMatchWholeWord(TRUE);
```

### See Also
- Everything_GetMatchWholeWord
- Everything_Query

## everything setmax

Source: https://www.voidtools.com/support/everything/sdk/everything_setmax

## Everything_SetMax
The Everything_SetMax function sets the maximum number of results to return from Everything_Query .

### Syntax
```
void Everything_SetMax(
    DWORD dwMaxResults
);
```

### Parameters
dwMaxResults

Specifies the maximum number of results to return.

Setting this to 0xffffffff will return all results.

### Remarks
The default maximum number of results is 0xffffffff (all results).

If you are displaying the results in a window, set the maximum number of results to the number of visible items in the window.

### Example
```
Everything_SetMax(window_height / item_height);
```

### See Also
- Everything_GetMax
- Everything_Query

## everything setoffset

Source: https://www.voidtools.com/support/everything/sdk/everything_setoffset

## Everything_SetOffset
The Everything_SetOffset function set the first result offset to return from a call to Everything_Query .

### Syntax
```
void Everything_SetOffset(
    DWORD dwOffset
);
```

### Parameters
dwOffset

Specifies the first result from the available results.

Set this to 0 to return the first available result.

### Remarks
The default offset is 0 (the first available result).

If you are displaying the results in a window with a custom scroll bar, set the offset to the vertical scroll bar position.

Using a search window can reduce the amount of data sent over the IPC and significantly increase search performance.

### Example
```
Everything_SetOffset(scrollbar_vpos);
```

### See Also
- Everything_GetOffset
- Everything_Query

## everything setregex

Source: https://www.voidtools.com/support/everything/sdk/everything_setregex

## Everything_SetRegex
The Everything_SetRegex function enables or disables Regular Expression searching.

### Syntax
```
void Everything_SetRegex(
    BOOL bEnabled
);
```

### Parameters
bEnabled

Set to non-zero to enable regex, set to zero to disable regex.

### Return Value
This function has no return value.

### Remarks
Regex is disabled by default.

### Example
```
Everything_SetRegex(TRUE);
```

### See Also
- Everything_GetRegex
- Everything_Query

## everything setreplyid

Source: https://www.voidtools.com/support/everything/sdk/everything_setreplyid

## Everything_SetReplyID
The Everything_SetReplyID function sets the unique number to identify the next query.

### Syntax
```
void Everything_SetReplyID(
    DWORD nId
);
```

### Parameters
nID

The unique number to identify the next query.

### Return Value
This function has no return value.

### Remarks
The default identifier is 0.

Set a unique identifier for the IPC Query.

If you want to post multiple search queries with the same window handle, you must call the Everything_SetReplyID function to assign each query a unique identifier.

The nID value is the dwData member in the COPYDATASTRUCT used in the WM_COPYDATA reply message.

This function is not required if you call Everything_Query with bWait set to true.

### Example
```
// reply to this window.
Everything_SetReplyWindow(hwnd);
// set a unique identifier for this query.
Everything_SetReplyID(1);
// execute the query
Everything_Query(FALSE);
```

### See Also
- Everything_Query
- Everything_SetReplyWindow
- Everything_GetReplyWindow
- Everything_GetReplyID
- Everything_IsQueryReply

## everything setreplywindow

Source: https://www.voidtools.com/support/everything/sdk/everything_setreplywindow

## Everything_SetReplyWindow
The Everything_SetReplyWindow function sets the window that will receive the the IPC Query results.

### Syntax
```
void Everything_SetReplyWindow(
    HWND hWnd
);
```

### Parameters
hWnd

The handle to the window that will receive the IPC Query reply.

### Return Value
This function has no return value.

### Remarks
This function must be called before calling Everything_Query with bWait set to FALSE.

Check for results with the specified window using Everything_IsQueryReply .

Call Everything_SetReplyID with a unique identifier to specify multiple searches.

### Example
```
// reply to this window.
Everything_SetReplyWindow(hwnd);
// execute the query
Everything_Query(TRUE);
```

### See Also
- Everything_Query
- Everything_SetReplyID
- Everything_GetReplyWindow
- Everything_GetReplyID
- Everything_IsQueryReply

## everything setrequestflags

Source: https://www.voidtools.com/support/everything/sdk/everything_setrequestflags

## Everything_SetRequestFlags
The Everything_SetRequestFlags function sets the desired result data.

### Syntax
```
void Everything_SetRequestFlags(
    DWORD dwRequestFlags
);
```

### Parameters
dwRequestFlags

The request flags, can be zero or more of the following flags:

```
EVERYTHING_REQUEST_FILE_NAME                            (0x00000001)
EVERYTHING_REQUEST_PATH                                 (0x00000002)
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME              (0x00000004)
EVERYTHING_REQUEST_EXTENSION                            (0x00000008)
EVERYTHING_REQUEST_SIZE                                 (0x00000010)
EVERYTHING_REQUEST_DATE_CREATED                         (0x00000020)
EVERYTHING_REQUEST_DATE_MODIFIED                        (0x00000040)
EVERYTHING_REQUEST_DATE_ACCESSED                        (0x00000080)
EVERYTHING_REQUEST_ATTRIBUTES                           (0x00000100)
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME                  (0x00000200)
EVERYTHING_REQUEST_RUN_COUNT                            (0x00000400)
EVERYTHING_REQUEST_DATE_RUN                             (0x00000800)
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED                (0x00001000)
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME                (0x00002000)
EVERYTHING_REQUEST_HIGHLIGHTED_PATH                     (0x00004000)
EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME  (0x00008000)
```

### Return Value
This function has no return value.

### Remarks
Make sure you include EVERYTHING_REQUEST_FILE_NAME and EVERYTHING_REQUEST_PATH if you want the result file name information returned.

The default request flags are EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH (0x00000003).

When the default flags (EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH) are used the SDK will use the old version 1 query.

When any other flags are used the new version 2 query will be tried first, and then fall back to version 1 query.

It is possible the requested data is not available, in which case after you have received your results you should call Everything_GetResultListRequestFlags to determine the available result data.

This function must be called before Everything_Query .

### Example
```
LARGE_INTEGER size;
// set the search.
Everything_SetSearch("123 ABC");
// request filename, path, size and date modified result data.
Everything_SetRequestFlags(EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH | EVERYTHING_REQUEST_SIZE | EVERYTHING_REQUEST_DATE_MODIFIED);
// execute the query
Everything_Query(TRUE);
// Get the size of the first result.
Everything_GetResultSize(0,&size);
```

### Requirements
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query
- Everything_GetResultListRequestFlags

## everything setruncountfromfilename

Source: https://www.voidtools.com/support/everything/sdk/everything_setruncountfromfilename

## Everything_SetRunCountFromFileName
The Everything_SetRunCountFromFileName function sets the run count for a specified file in the Everything index by file name.

### Syntax
```
BOOL Everything_SetRunCountFromFileName(
    LPCTSTR lpFileName,
    DWORD dwRunCount
);
```

### Parameters
lpFileName [in]

Pointer to a null-terminated string that specifies a fully qualified file name in the Everything index.

dwRunCount [in]

The new run count.

### Return Value
The function returns non-zero if successful.

The function returns 0 if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Set the run count to 0 to remove any run history information for the specified file.

The file does not have to exist. When the file is created it will have the correct run history.

Run history information is preserved between file deletion and creation.

Calling this function will update the date run to the current time for the specified file.

### Example
```
// set a file to show higher in the results by setting an exaggerated run count
Everything_SetRunCountFromFileName(TEXT("C:\\folder\\file.doc"),1000);
```

### See Also
- Everything_GetRunCountFromFileName
- Everything_IncRunCountFromFileName

## everything setsearch

Source: https://www.voidtools.com/support/everything/sdk/everything_setsearch

## Everything_SetSearch
The Everything_SetSearch function sets the search string for the IPC Query.

### Syntax
```
void Everything_SetSearch(
    LPCTSTR lpString
);
```

### Parameters
lpString [in]

Pointer to a null-terminated string to be used as the new search text.

### Return Value
This function has no return value.

### Remarks
Optionally call this function prior to a call to Everything_Query

Everything_Query executes the IPC Query using this search string.

### Example
```
// Set the search string to abc AND 123
Everything_SetSearch("abc 123");
// Execute the IPC query.
Everything_Query(TRUE);
```

### See Also
- Everything_GetSearch
- Everything_Query

## everything setsort

Source: https://www.voidtools.com/support/everything/sdk/everything_setsort

## Everything_SetSort
The Everything_SetSort function sets how the results should be ordered.

### Syntax
```
void Everything_SetSort(
    DWORD dwSortType
);
```

### Parameters
dwSortType

The sort type, can be one of the following values:

```
EVERYTHING_SORT_NAME_ASCENDING                      (1)
EVERYTHING_SORT_NAME_DESCENDING                     (2)
EVERYTHING_SORT_PATH_ASCENDING                      (3)
EVERYTHING_SORT_PATH_DESCENDING                     (4)
EVERYTHING_SORT_SIZE_ASCENDING                      (5)
EVERYTHING_SORT_SIZE_DESCENDING                     (6)
EVERYTHING_SORT_EXTENSION_ASCENDING                 (7)
EVERYTHING_SORT_EXTENSION_DESCENDING                (8)
EVERYTHING_SORT_TYPE_NAME_ASCENDING                 (9)
EVERYTHING_SORT_TYPE_NAME_DESCENDING                (10)
EVERYTHING_SORT_DATE_CREATED_ASCENDING              (11)
EVERYTHING_SORT_DATE_CREATED_DESCENDING             (12)
EVERYTHING_SORT_DATE_MODIFIED_ASCENDING             (13)
EVERYTHING_SORT_DATE_MODIFIED_DESCENDING            (14)
EVERYTHING_SORT_ATTRIBUTES_ASCENDING                (15)
EVERYTHING_SORT_ATTRIBUTES_DESCENDING               (16)
EVERYTHING_SORT_FILE_LIST_FILENAME_ASCENDING        (17)
EVERYTHING_SORT_FILE_LIST_FILENAME_DESCENDING       (18)
EVERYTHING_SORT_RUN_COUNT_ASCENDING                 (19)
EVERYTHING_SORT_RUN_COUNT_DESCENDING                (20)
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_ASCENDING     (21)
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_DESCENDING    (22)
EVERYTHING_SORT_DATE_ACCESSED_ASCENDING             (23)
EVERYTHING_SORT_DATE_ACCESSED_DESCENDING            (24)
EVERYTHING_SORT_DATE_RUN_ASCENDING                  (25)
EVERYTHING_SORT_DATE_RUN_DESCENDING                 (26)
```

### Return Value
This function has no return value.

### Remarks
The default sort is EVERYTHING_SORT_NAME_ASCENDING (1). This sort is free.

Using fast sorts is recommended, fast sorting is instant.

To enable fast sorts in Everything:

- In Everything , from the Tools menu, click Options .
- Click the Indexes tab.
- Check fast sort for desired fast sort type.
- Click OK .

It is possible the sort is not supported, in which case after you have received your results you should call * Everything_GetResultListSort to determine the sorting actually used.

This function must be called before Everything_Query .

### Example
```
// set the search.
Everything_SetSearch("123 ABC");
// sort by size descending.
Everything_SetSort(EVERYTHING_SORT_SIZE_DESCENDING);
// execute the query
Everything_Query(TRUE);
```

### Requirements
Requires Everything 1.4.1 or later.

### See Also
- Everything_Query

## everything sortresultsbypath

Source: https://www.voidtools.com/support/everything/sdk/everything_sortresultsbypath

## Everything_SortResultsByPath
The Everything_SortResultsByPath function sorts the current results by path, then file name.

SortResultsByPath is CPU Intensive. Sorting by path can take several seconds.

### Syntax
```
void Everything_SortResultsByPath(void);
```

### Parameters
This functions has no parameters.

### Return Value
This function has no return value.

### Remarks
The default result list contains no results.

Call Everything_Query to retrieve the result list prior to a call to Everything_SortResultsByPath.

For improved performance, use [Everything/SDK/Everything_SetSort|Everything_SetSort]]

### Example
```
// set the search text to abc AND 123
Everything_SetSearch(\"abc 123\");
// execute the query
Everything_Query(TRUE);
// sort the results by path
Everything_SortResultsByPath();
```

### See Also
- Everything_Query

## everything updateallfolderindexes

Source: https://www.voidtools.com/support/everything/sdk/everything_updateallfolderindexes

## Everything_UpdateAllFolderIndexes
The Everything_UpdateAllFolderIndexes function requests Everything to rescan all folder indexes.

### Syntax
```
BOOL Everything_UpdateAllFolderIndexes(void);
```

### Parameters
No parameters.

### Return Value
The function returns non-zero if the request to rescan all folder indexes was successful.

The function returns 0 if an error occurred. To get extended error information, call Everything_GetLastError

Error code
Meaning
EVERYTHING_ERROR_IPC
Please make sure the Everything search client is running in the background.
### Remarks
Everything will begin updating all folder indexes in the background.

### Example
```
// Request all folder indexes be rescanned.
Everything_UpdateAllFolderIndexes();
```

### Function Information
Requires Everything 1.4.1 or later.

### See Also

