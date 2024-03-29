#!/usr/bin/env node

const { exec, spawn } = require('child_process');
const { copyFileSync, unlinkSync } = require('fs');
const MAX_TC = 20;

const argv = process.argv.slice(2)

function doProcess(pass) {
    console.log(`------------------------\nTC ${pass}\n`);
    child = exec('clips -f2 kbs.clp', (err, stdout, stderr) => {
        console.log(stdout);
    });
    child.stdin.write(`(load tc${pass}.clp)\n`);
    child.stdin.write('(reset)\n');
    child.stdin.write('(run)\n');
    child.stdin.write('(exit)\n');

    child.on('exit', () => {
        setTimeout(() => {
            pass++;
            if (pass <= MAX_TC) {
                console.log('\n\n');
                doProcess(pass)
            } else {
                unlinkSync('kbs.clp');
            }
        }, 100);
    })
}

if (argv.length === 0) {
    copyFileSync('../knowledge_base.clp', 'kbs.clp');
    doProcess(1);
} else {
    console.log(`Wrong paramater, expected 0 argument, got ${argv.length} argument(s)`);
}