# Connection Portal Integration (docs.snaptrade.com/docs/implement-connection-portal)

Source: https://docs.snaptrade.com/docs/implement-connection-portal

## Methods
1) Regular web browser (new tab/window)
2) React SDK (iframe integration)
3) iFrame (non-React)
4) React Native WebView
5) iOS WebView
6) Android WebView

## Client-side window messages
- SUCCESS: {status:'SUCCESS', authorizationId:'AUTHORIZATION_ID'}
- ERROR: {status:'ERROR', errorCode:'ERROR_CODE', statusCode:'STATUS_CODE', detail:'DETAIL'}
- CLOSED / CLOSE_MODAL / ABANDONED

Use these messages to detect completion or failure of the connection flow.
