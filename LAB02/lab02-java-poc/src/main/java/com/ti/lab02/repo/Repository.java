package com.ti.lab02.repo;

import com.ti.lab02.ckmetric.CKMetric;
import com.ti.lab02.global.domain.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import static com.ti.lab02.utils.HashUtils.generateHash;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "t_repository", uniqueConstraints = {
        @UniqueConstraint(name = "uk_repository_hash_id", columnNames = {"hash_id"}),
        @UniqueConstraint(name = "uk_repository", columnNames = {"id"})
})
@SQLDelete(sql = "UPDATE t_repository SET deleted = true WHERE id = ?")
@Where(clause = "deleted = false")
@ToString(of = {"id", "hashId"})
@EqualsAndHashCode(of = "id", callSuper = false)
public class Repository extends BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "id")
    private long id;

    @Builder.Default
    @Column(name = "hash_id")
    private String hashId = generateHash();

    @Column(name = "name")
    private String name;

    @Column(name = "name_with_owner")
    private String nameWithOwner;

    @Column(name = "url")
    private String url;

    @Column(name = "disk_usage")
    private long diskUsage;

    @Column(name = "release_total_count")
    private long releaseTotalCount;

    @Column(name = "stargazer_total_count")
    private long startgazerTotalCount;

    @OneToOne(mappedBy = "repository", fetch = FetchType.EAGER)
    private CKMetric ckMetric;

}
