# Logs

## Robot was often spinning in one cell

- made dwell penalty greater than revisit penalty: Failed
- added normalized dwell to observation vector; kept the increased dwell penalty: Success

## Robot gets stuck in loops when all surrounding cells are visited

- make revisit penalty 0 when all surrounding cells are visited: Success
    loops less likely, but still happenning
