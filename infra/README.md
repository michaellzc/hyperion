# Infrastructure

## Deployment

```bash
# Create env file for specific environment
$ cp .env.example prod.env

# Edit env var as needed
$ vim prod.env

# Start production database instance
$ env $(cat prod.env) docker-compose -f docker-compose.yml -p <project_name> up -d
```

## Connection Info

Production database

`postgres://<username>:<password>@yeg02.pub.vfree.org:5432/postgres`

Staging database

`postgres://<username>:<password>@yeg02.pub.vfree.org:5433/postgres`

Development database

`postgres://<username>:<password>@yeg02.pub.vfree.org:5434/postgres`
